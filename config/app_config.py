"""
Application configuration management.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any
import json
import logging
from enum import Enum


class LogLevel(Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class AppConfig:
    """
    Application configuration settings.
    """
    
    # Application settings
    app_name: str = "Hiel PDF Converter"
    app_version: str = "1.0.0"
    
    # Window settings
    window_width: int = 1000
    window_height: int = 700
    window_min_width: int = 800
    window_min_height: int = 600
    
    # Default paths
    default_output_directory: Optional[Path] = None
    last_input_directory: Optional[Path] = None
    last_output_directory: Optional[Path] = None
    
    # Conversion settings
    default_conversion_type: str = "text"
    image_dpi: int = 300
    
    # Logging settings
    log_level: LogLevel = LogLevel.INFO
    log_file: Optional[Path] = None
    
    # UI settings
    theme_mode: str = "light"  # light, dark, system
    language: str = "en"
    
    def __post_init__(self):
        """Initialize configuration after creation."""
        self.logger = logging.getLogger(__name__)
        
        # Set default paths
        if self.default_output_directory is None:
            self.default_output_directory = Path.home() / "Documents" / "PDF Conversions"
        
        if self.log_file is None:
            self.log_file = Path.home() / ".hiel_converter" / "app.log"
        
        # Ensure paths are Path objects
        if isinstance(self.default_output_directory, str):
            self.default_output_directory = Path(self.default_output_directory)
        
        if isinstance(self.log_file, str):
            self.log_file = Path(self.log_file)
        
        # Create directories if they don't exist
        self.default_output_directory.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Set up application logging."""
        logging.basicConfig(
            level=getattr(logging, self.log_level.value),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
    
    @classmethod
    def load_from_file(cls, config_file: Path) -> 'AppConfig':
        """
        Load configuration from a JSON file.
        
        Args:
            config_file: Path to the configuration file
            
        Returns:
            AppConfig instance with loaded settings
        """
        try:
            if not config_file.exists():
                return cls()
            
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Convert path strings to Path objects
            if 'default_output_directory' in config_data:
                config_data['default_output_directory'] = Path(config_data['default_output_directory'])
            
            if 'last_input_directory' in config_data:
                config_data['last_input_directory'] = Path(config_data['last_input_directory'])
            
            if 'last_output_directory' in config_data:
                config_data['last_output_directory'] = Path(config_data['last_output_directory'])
            
            if 'log_file' in config_data:
                config_data['log_file'] = Path(config_data['log_file'])
            
            # Convert log level string to enum
            if 'log_level' in config_data:
                config_data['log_level'] = LogLevel(config_data['log_level'])
            
            return cls(**config_data)
            
        except Exception as e:
            logging.error(f"Error loading configuration: {str(e)}")
            return cls()
    
    def save_to_file(self, config_file: Path):
        """
        Save configuration to a JSON file.
        
        Args:
            config_file: Path to save the configuration file
        """
        try:
            # Ensure config directory exists
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to dictionary
            config_data = {
                'app_name': self.app_name,
                'app_version': self.app_version,
                'window_width': self.window_width,
                'window_height': self.window_height,
                'window_min_width': self.window_min_width,
                'window_min_height': self.window_min_height,
                'default_output_directory': str(self.default_output_directory),
                'last_input_directory': str(self.last_input_directory) if self.last_input_directory else None,
                'last_output_directory': str(self.last_output_directory) if self.last_output_directory else None,
                'default_conversion_type': self.default_conversion_type,
                'image_dpi': self.image_dpi,
                'log_level': self.log_level.value,
                'log_file': str(self.log_file),
                'theme_mode': self.theme_mode,
                'language': self.language
            }
            
            # Remove None values
            config_data = {k: v for k, v in config_data.items() if v is not None}
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"Configuration saved to {config_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving configuration: {str(e)}")
    
    def get_config_file_path(self) -> Path:
        """
        Get the default configuration file path.
        
        Returns:
            Path to the configuration file
        """
        return Path.home() / ".hiel_converter" / "config.json"
    
    def update_last_directories(self, input_dir: Optional[Path] = None, output_dir: Optional[Path] = None):
        """
        Update the last used directories.
        
        Args:
            input_dir: Last input directory
            output_dir: Last output directory
        """
        if input_dir:
            self.last_input_directory = input_dir
        
        if output_dir:
            self.last_output_directory = output_dir
        
        # Auto-save configuration
        self.save_to_file(self.get_config_file_path())
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get supported languages.
        
        Returns:
            Dictionary of language codes to names
        """
        return {
            'en': 'English',
            'ar': 'العربية',
            'fr': 'Français',
            'es': 'Español',
            'de': 'Deutsch'
        }
    
    def get_supported_themes(self) -> Dict[str, str]:
        """
        Get supported themes.
        
        Returns:
            Dictionary of theme codes to names
        """
        return {
            'light': 'Light',
            'dark': 'Dark',
            'system': 'System'
        }