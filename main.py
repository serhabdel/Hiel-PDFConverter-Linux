#!/usr/bin/env python3
"""
Hiel PDF Converter - Main Application Entry Point
A desktop application for converting PDF files to various formats using Flet.
"""

import flet as ft
from pathlib import Path
from presentation.main_view import MainView
from infrastructure.pdf_repository_impl import PDFRepositoryImpl
from infrastructure.converter_factory import ConverterFactory
from config.app_config import AppConfig


def main(page: ft.Page):
    """Main application entry point."""
    
    # Configure the main page
    page.title = "Hiel PDF Converter"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1000
    page.window_height = 650  # Slightly smaller to show scrolling
    page.window_min_width = 800
    page.window_min_height = 500  # Smaller minimum height
    page.padding = 0
    page.spacing = 0
    
    # Set app icon if available
    page.window_icon = "assets/icon.ico" if Path("assets/icon.ico").exists() else None
    
    # Initialize configuration
    config = AppConfig()
    
    # Initialize dependencies
    pdf_repository = PDFRepositoryImpl()
    converter_factory = ConverterFactory()
    
    # Create and display main view
    main_view = MainView(
        page=page,
        pdf_repository=pdf_repository,
        converter_factory=converter_factory,
        config=config
    )
    
    # Build and add the main view to the page
    page.add(main_view.build())
    
    # Set up page events
    page.on_route_change = main_view.route_change
    page.on_view_pop = main_view.view_pop
    
    # Navigate to home
    page.go("/")


if __name__ == "__main__":
    print("Starting Hiel PDF Converter...")
    ft.app(target=main)