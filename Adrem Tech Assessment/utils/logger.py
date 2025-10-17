"""
Logger utility module for test execution logging
Implements centralized logging with color-coded output
"""
import logging
import os
from datetime import datetime
import colorlog


class Logger:
    """Centralized logger class for test automation framework"""
    
    _logger = None
    
    @staticmethod
    def get_logger(name=__name__, log_level=logging.DEBUG):
        """
        Creates and returns a configured logger instance
        
        Args:
            name: Logger name
            log_level: Logging level (default: DEBUG)
            
        Returns:
            Configured logger instance
        """
        if Logger._logger is not None:
            return Logger._logger
            
        Logger._logger = logging.getLogger(name)
        Logger._logger.setLevel(log_level)
        
        # Prevent duplicate handlers
        if Logger._logger.handlers:
            return Logger._logger
        
        # Console Handler with color formatting
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - [%(levelname)s] - %(name)s - %(message)s%(reset)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_formatter)
        Logger._logger.addHandler(console_handler)
        
        # File Handler
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f'automation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        file_formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - %(name)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        Logger._logger.addHandler(file_handler)
        
        return Logger._logger
    
    @staticmethod
    def reset_logger():
        """Reset logger instance - useful for testing"""
        Logger._logger = None


# Module-level logger instance for easy importing
logger = Logger.get_logger(__name__)
