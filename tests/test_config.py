"""Tests for configuration management."""

import os
import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch
from function_monitor.config import MonitorConfig, configure_monitor, get_config


class TestMonitorConfig:
    """Test MonitorConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = MonitorConfig()
        
        assert config.default_validate_input is True
        assert config.default_validate_output is True
        assert config.default_log_execution is True
        assert config.enable_memory_monitoring is True
        assert config.enable_cpu_monitoring is True
    
    def test_config_from_dict(self):
        """Test creating config from dictionary."""
        config_dict = {
            "log_level": 10,
            "log_to_file": True,
            "default_validate_input": False
        }
        
        config = MonitorConfig.from_dict(config_dict)
        
        assert config.log_level == 10
        assert config.log_to_file is True
        assert config.default_validate_input is False
    
    def test_config_update(self):
        """Test updating configuration."""
        config = MonitorConfig()
        
        config.update(
            log_level=20,
            default_return_raw_result=True
        )
        
        assert config.log_level == 20
        assert config.default_return_raw_result is True
    
    def test_config_update_invalid_key(self):
        """Test updating with invalid key raises error."""
        config = MonitorConfig()
        
        with pytest.raises(ValueError, match="Unknown configuration key"):
            config.update(invalid_key="value")
    
    def test_log_file_directory_creation(self):
        """Test that log file directory is created."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "subdir" / "test.log"
            
            config = MonitorConfig(
                log_to_file=True,
                log_file_path=str(log_file)
            )
            
            # Directory should be created during post_init
            assert log_file.parent.exists()


class TestConfigureFunctions:
    """Test configuration utility functions."""
    
    def test_configure_monitor(self):
        """Test configure_monitor function."""
        configure_monitor(
            log_level=10,
            log_to_file=True,
            default_validate_input=False
        )
        
        config = get_config()
        assert config.log_level == 10
        assert config.log_to_file is True
        assert config.default_validate_input is False
    
    def test_environment_variables(self):
        """Test configuration from environment variables."""
        env_vars = {
            "FUNCTION_MONITOR_LOG_LEVEL": "10",
            "FUNCTION_MONITOR_LOG_TO_FILE": "true",
            "FUNCTION_MONITOR_LOG_FILE": "/tmp/test.log"
        }
        
        with patch.dict(os.environ, env_vars):
            config = MonitorConfig.from_env()
            
            assert config.log_level == 10
            assert config.log_to_file is True
            assert config.log_file_path == "/tmp/test.log"