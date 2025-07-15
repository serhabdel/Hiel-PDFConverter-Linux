"""
Main view component for the Hiel PDF Converter application.
"""

import flet as ft
from pathlib import Path
from typing import Optional
import logging

from domain.entities import PDFDocument
from domain.value_objects import ConversionOptions, ConversionType
from domain.interfaces.repository import PDFRepository
from infrastructure.converter_factory import ConverterFactory
from config.app_config import AppConfig
from use_cases.convert_pdf_use_case import ConvertPDFUseCase


class MainView:
    """
    Main view component containing the PDF converter interface.
    """
    
    def __init__(self, page: ft.Page, pdf_repository: PDFRepository, 
                 converter_factory: ConverterFactory, config: AppConfig):
        self.page = page
        self.pdf_repository = pdf_repository
        self.converter_factory = converter_factory
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize use case
        self.convert_use_case = ConvertPDFUseCase(pdf_repository, converter_factory)
        
        # State variables
        self.current_pdf: Optional[PDFDocument] = None
        self.conversion_in_progress = False
        
        # UI components
        self.file_picker = ft.FilePicker(on_result=self.pick_file_result)
        self.output_picker = ft.FilePicker(on_result=self.pick_output_result)
        self.pdf_info_text = ft.Text("No PDF selected", size=14)
        self.conversion_type_dropdown = ft.Dropdown(
            label="Conversion Type",
            options=[
                ft.dropdown.Option(ConversionType.TEXT.value, "Plain Text"),
                ft.dropdown.Option(ConversionType.WORD.value, "Word Document"),
                ft.dropdown.Option(ConversionType.HTML.value, "HTML"),
                ft.dropdown.Option(ConversionType.MARKDOWN.value, "Markdown"),
                ft.dropdown.Option(ConversionType.IMAGE.value, "Images"),
            ],
            value=ConversionType.TEXT.value,
            width=200,
            on_change=self.conversion_type_changed
        )
        
        # Image quality options (initially hidden)
        self.image_quality_dropdown = ft.Dropdown(
            label="Quality Preset",
            options=[
                ft.dropdown.Option("low", "Low (72 DPI, JPEG 60%)"),
                ft.dropdown.Option("medium", "Medium (150 DPI, JPEG 85%)"),
                ft.dropdown.Option("high", "High (200 DPI, JPEG 95%)"),
                ft.dropdown.Option("ultra", "Ultra (300 DPI, PNG)"),
                ft.dropdown.Option("custom", "Custom Settings"),
            ],
            value="medium",
            width=220,
            visible=False,
            on_change=self.quality_preset_changed
        )
        
        # Advanced image settings (initially hidden)
        self.image_format_dropdown = ft.Dropdown(
            label="Format",
            options=[
                ft.dropdown.Option("JPEG", "JPEG (Smaller)"),
                ft.dropdown.Option("PNG", "PNG (Lossless)"),
            ],
            value="JPEG",
            width=150,
            visible=False
        )
        
        self.image_dpi_field = ft.TextField(
            label="DPI",
            value="150",
            width=100,
            visible=False,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        self.image_quality_slider = ft.Slider(
            min=10,
            max=100,
            value=85,
            divisions=18,
            label="Quality: {value}%",
            width=200,
            visible=False,
            on_change=self.quality_slider_changed
        )
        
        self.quality_label = ft.Text("Quality: 85%", size=12, visible=False)
        
        # Advanced settings container
        self.advanced_settings = ft.Container(
            content=ft.Column([
                ft.Text("Advanced Settings", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([
                    self.image_format_dropdown,
                    ft.Container(width=10),
                    self.image_dpi_field,
                    ft.Container(width=10),
                    ft.Column([
                        self.quality_label,
                        self.image_quality_slider
                    ])
                ])
            ]),
            padding=ft.padding.all(10),
            border=ft.border.all(1, "grey"),
            border_radius=8,
            visible=False
        )
        
        # File size estimation
        self.size_estimate_text = ft.Text("", size=12, color="blue", visible=False)
        self.output_path_text = ft.Text("No output path selected", size=14)
        self.convert_button = ft.ElevatedButton(
            "🚀 Convert PDF",
            on_click=self.convert_pdf,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor="orange",
                color="white",
                padding=ft.padding.symmetric(horizontal=30, vertical=15),
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
            )
        )
        self.progress_bar = ft.ProgressBar(visible=False)
        self.status_text = ft.Text("Ready", size=14, color="green")
        
        # Add file pickers to page overlay
        self.page.overlay.extend([self.file_picker, self.output_picker])
    
    def conversion_type_changed(self, e):
        """Handle conversion type change to show/hide image quality options."""
        if self.conversion_type_dropdown.value == ConversionType.IMAGE.value:
            self.image_quality_dropdown.visible = True
            self.size_estimate_text.visible = True
            self._update_size_estimate()
        else:
            self.image_quality_dropdown.visible = False
            self.advanced_settings.visible = False
            self.size_estimate_text.visible = False
        
        self.page.update()
    
    def quality_preset_changed(self, e):
        """Handle quality preset change."""
        preset = self.image_quality_dropdown.value
        
        if preset == "custom":
            self.advanced_settings.visible = True
        else:
            self.advanced_settings.visible = False
            
            # Update advanced settings based on preset
            presets = {
                "low": {"dpi": "72", "format": "JPEG", "quality": 60},
                "medium": {"dpi": "150", "format": "JPEG", "quality": 85},
                "high": {"dpi": "200", "format": "JPEG", "quality": 95},
                "ultra": {"dpi": "300", "format": "PNG", "quality": 95}
            }
            
            if preset in presets:
                settings = presets[preset]
                self.image_dpi_field.value = settings["dpi"]
                self.image_format_dropdown.value = settings["format"]
                self.image_quality_slider.value = settings["quality"]
                self.quality_label.value = f"Quality: {settings['quality']}%"
                
                # Hide quality slider for PNG
                self.image_quality_slider.visible = settings["format"] == "JPEG"
                self.quality_label.visible = settings["format"] == "JPEG"
        
        self._update_size_estimate()
        self.page.update()
    
    def quality_slider_changed(self, e):
        """Handle quality slider change."""
        quality = int(self.image_quality_slider.value)
        self.quality_label.value = f"Quality: {quality}%"
        self._update_size_estimate()
        self.page.update()
    
    def _update_size_estimate(self):
        """Update file size estimation."""
        if not self.current_pdf or self.conversion_type_dropdown.value != ConversionType.IMAGE.value:
            return
        
        try:
            # Get current settings
            if self.image_quality_dropdown.value == "custom":
                dpi = int(self.image_dpi_field.value) if self.image_dpi_field.value.isdigit() else 150
                format_type = self.image_format_dropdown.value
                quality = int(self.image_quality_slider.value)
            else:
                presets = {
                    "low": {"dpi": 72, "format": "JPEG", "quality": 60},
                    "medium": {"dpi": 150, "format": "JPEG", "quality": 85},
                    "high": {"dpi": 200, "format": "JPEG", "quality": 95},
                    "ultra": {"dpi": 300, "format": "PNG", "quality": 95}
                }
                preset = presets.get(self.image_quality_dropdown.value, presets["medium"])
                dpi = preset["dpi"]
                format_type = preset["format"]
                quality = preset["quality"]
            
            # Estimate file size
            pages = self.current_pdf.pages
            
            if format_type == "JPEG":
                # JPEG estimation: base size per page * DPI factor * quality factor
                base_size = 200_000  # 200KB base
                dpi_factor = (dpi / 150) ** 2  # Quadratic scaling with DPI
                quality_factor = quality / 85.0  # Linear scaling with quality
                size_per_page = base_size * dpi_factor * quality_factor
            else:  # PNG
                # PNG estimation: larger base size, only DPI matters
                base_size = 800_000  # 800KB base
                dpi_factor = (dpi / 150) ** 2
                size_per_page = base_size * dpi_factor
            
            total_size = size_per_page * pages
            
            # Format size
            if total_size < 1024:
                size_str = f"{total_size:.0f} B"
            elif total_size < 1024 * 1024:
                size_str = f"{total_size / 1024:.1f} KB"
            else:
                size_str = f"{total_size / (1024 * 1024):.1f} MB"
            
            self.size_estimate_text.value = f"Estimated size: {size_str} ({pages} pages)"
            
        except Exception as e:
            self.size_estimate_text.value = "Size estimation unavailable"
    
    def build(self):
        """Build the main view UI."""
        main_content = ft.Column([
            # Modern Header with gradient-like styling
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("📄", size=40),
                        ft.Column([
                            ft.Text("Hiel PDF Converter", size=28, weight=ft.FontWeight.BOLD, color="blue"),
                            ft.Text("Convert your PDFs with precision", size=14, color="grey")
                        ], spacing=0)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.all(20),
                bgcolor="lightblue",
                border_radius=12,
                margin=ft.margin.only(bottom=20)
            ),
            
            # File selection section with modern styling
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("📁", size=20),
                            ft.Text("Select PDF File", size=18, weight=ft.FontWeight.BOLD, color="blue"),
                        ], spacing=8),
                        ft.Container(height=10),
                        ft.Row([
                            ft.ElevatedButton(
                                "📁 Browse PDF",
                                on_click=lambda _: self.file_picker.pick_files(
                                    allow_multiple=False,
                                    allowed_extensions=["pdf"]
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor="blue",
                                    color="white",
                                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                                )
                            ),
                            ft.Container(
                                content=self.pdf_info_text,
                                expand=True,
                                padding=ft.padding.only(left=20)
                            )
                        ], alignment=ft.MainAxisAlignment.START)
                    ]),
                    padding=20
                ),
                elevation=2
            ),
            
            # Conversion options section with modern styling
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("⚙️", size=20),
                            ft.Text("Conversion Options", size=18, weight=ft.FontWeight.BOLD, color="blue"),
                        ], spacing=8),
                        ft.Container(height=15),
                        ft.Row([
                            self.conversion_type_dropdown,
                            ft.Container(width=20),  # Spacer
                            self.image_quality_dropdown,
                            ft.Container(width=20),  # Spacer
                            ft.ElevatedButton(
                                "💾 Select Output Location",
                                on_click=self.pick_output_location,
                                style=ft.ButtonStyle(
                                    bgcolor="green",
                                    color="white",
                                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                                )
                            )
                        ]),
                        
                        # Advanced image settings
                        ft.Container(
                            content=self.advanced_settings,
                            padding=ft.padding.only(top=10)
                        ),
                        
                        # File size estimation
                        ft.Container(
                            content=self.size_estimate_text,
                            padding=ft.padding.only(top=10)
                        ),
                        
                        ft.Container(
                            content=self.output_path_text,
                            padding=ft.padding.only(top=10)
                        )
                    ]),
                    padding=20
                ),
                elevation=2
            ),
            
            # Conversion section with modern styling
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("🔄", size=20),
                            ft.Text("Convert", size=18, weight=ft.FontWeight.BOLD, color="blue"),
                        ], spacing=8),
                        ft.Container(height=15),
                        ft.Row([
                            self.convert_button,
                            ft.Container(width=20),  # Spacer
                            ft.Container(
                                content=self.status_text,
                                expand=True
                            )
                        ]),
                        ft.Container(
                            content=self.progress_bar,
                            padding=ft.padding.only(top=10)
                        )
                    ]),
                    padding=20
                ),
                elevation=2
            ),
            
            # Footer
            ft.Container(
                content=ft.Text(
                    "Hiel PDF Converter - Convert your PDF files to various formats",
                    size=12,
                    color="grey",
                    text_align=ft.TextAlign.CENTER
                ),
                padding=ft.padding.only(top=20, bottom=40),
                alignment=ft.alignment.center
            )
        ], spacing=20)
        
        # Create a scrollable ListView with better spacing
        scrollable_content = ft.ListView(
            controls=[main_content],
            spacing=0,
            padding=ft.padding.all(20),
            expand=True,
            auto_scroll=False,
            # Add some breathing room at the bottom
            width=None,
            height=None
        )
        
        return scrollable_content
    
    def pick_file_result(self, e: ft.FilePickerResultEvent):
        """Handle PDF file selection result."""
        if e.files:
            try:
                file_path = Path(e.files[0].path)
                self.current_pdf = self.pdf_repository.load_pdf(file_path)
                
                # Set default output path to same directory as input file
                default_output_name = f"{self.current_pdf.path.stem}_converted"
                default_output_path = self.current_pdf.path.parent / default_output_name
                self.output_path_text.value = f"Output: {default_output_path}"
                self.output_path_text.color = "green"
                
                # Update UI
                self.pdf_info_text.value = f"Selected: {self.current_pdf.filename} ({self.current_pdf.pages} pages)"
                self.pdf_info_text.color = "green"
                
                # Update size estimation if image conversion is selected
                if self.conversion_type_dropdown.value == ConversionType.IMAGE.value:
                    self._update_size_estimate()
                
                self.update_convert_button_state()
                self.page.update()
                
            except Exception as ex:
                self.show_error(f"Error loading PDF: {str(ex)}")
    
    def pick_output_location(self, e):
        """Handle output location selection."""
        # Set default filename based on input PDF
        default_filename = "converted_file"
        initial_directory = None
        
        if self.current_pdf:
            default_filename = f"{self.current_pdf.path.stem}_converted"
            initial_directory = str(self.current_pdf.path.parent)
        
        self.output_picker.save_file(
            dialog_title="Select output location",
            file_name=default_filename,
            initial_directory=initial_directory
        )
    
    def pick_output_result(self, e: ft.FilePickerResultEvent):
        """Handle output location selection result."""
        if e.path:
            self.output_path_text.value = f"Output: {e.path}"
            self.output_path_text.color = "green"
            self.update_convert_button_state()
            self.page.update()
    
    def update_convert_button_state(self):
        """Update the convert button enabled state."""
        has_output_path = (
            self.output_path_text.value != "No output path selected" and
            self.output_path_text.value.startswith("Output: ")
        )
        
        self.convert_button.disabled = (
            self.current_pdf is None or 
            not has_output_path or
            self.conversion_in_progress
        )
    
    def convert_pdf(self, e):
        """Handle PDF conversion."""
        if not self.current_pdf or not self.output_path_text.value.startswith("Output: "):
            return
        
        try:
            # Set conversion in progress
            self.conversion_in_progress = True
            self.update_convert_button_state()
            self.progress_bar.visible = True
            self.status_text.value = "Converting..."
            self.status_text.color = "blue"
            self.page.update()
            
            # Get conversion options
            conversion_type = ConversionType(self.conversion_type_dropdown.value)
            output_path = Path(self.output_path_text.value.replace("Output: ", ""))
            
            # Get image quality if converting to images
            image_quality = None
            image_dpi = None
            image_format = None
            image_compression_quality = None
            
            if conversion_type == ConversionType.IMAGE:
                if self.image_quality_dropdown.value == "custom":
                    image_quality = "custom"
                    image_dpi = int(self.image_dpi_field.value) if self.image_dpi_field.value.isdigit() else 150
                    image_format = self.image_format_dropdown.value
                    image_compression_quality = int(self.image_quality_slider.value)
                else:
                    image_quality = self.image_quality_dropdown.value
            
            options = ConversionOptions(
                type=conversion_type,
                output_path=output_path,
                image_quality=image_quality
            )
            
            # Add custom settings as attributes (for backward compatibility)
            if image_dpi is not None:
                object.__setattr__(options, 'image_dpi', image_dpi)
            if image_format is not None:
                object.__setattr__(options, 'image_format', image_format)
            if image_compression_quality is not None:
                object.__setattr__(options, 'image_compression_quality', image_compression_quality)
            
            # Perform conversion
            result_path = self.convert_use_case.execute(self.current_pdf, options)
            
            # Update UI on success
            self.status_text.value = f"Conversion completed! Saved to: {result_path}"
            self.status_text.color = "green"
            
            # Show success dialog
            self.show_success(f"PDF converted successfully to {result_path}")
            
        except Exception as ex:
            self.show_error(f"Conversion failed: {str(ex)}")
        
        finally:
            # Reset UI state
            self.conversion_in_progress = False
            self.progress_bar.visible = False
            self.update_convert_button_state()
            self.page.update()
    
    def show_error(self, message: str):
        """Show error message to user."""
        self.status_text.value = f"Error: {message}"
        self.status_text.color = "red"
        
        # Show error dialog
        dlg = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda _: self.page.close(dlg))]
        )
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()
    
    def show_success(self, message: str):
        """Show success message to user."""
        # Show success dialog
        dlg = ft.AlertDialog(
            title=ft.Text("Success"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda _: self.page.close(dlg))]
        )
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()
    
    def route_change(self, route):
        """Handle route changes."""
        pass
    
    def view_pop(self, view):
        """Handle view pop events."""
        pass