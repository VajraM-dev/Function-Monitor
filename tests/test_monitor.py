"""Tests for the function monitor."""

import pytest
import time
from unittest.mock import patch, MagicMock
from pydantic import BaseModel

from function_monitor import monitor_function, FunctionMonitor, configure_monitor
from function_monitor.models import ExecutionResult


class TestUser(BaseModel):
    name: str
    age: int


class TestMonitorFunction:
    """Test the monitor_function decorator."""
    
    def test_basic_monitoring(self):
        """Test basic function monitoring."""
        @monitor_function()
        def add(a: int, b: int) -> int:
            return a + b
        
        result = add(2, 3)
        
        assert isinstance(result, dict)
        assert result["status"] == "success"
        assert result["result"] == 5
        assert result["function_name"] == "add"
        assert "execution_time" in result
        assert "memory_usage" in result
    
    def test_return_raw_result(self):
        """Test returning raw result on success."""
        @monitor_function(return_raw_result=True)
        def multiply(a: int, b: int) -> int:
            return a * b
        
        result = multiply(3, 4)
        assert result == 12
    
    def test_function_with_error(self):
        """Test monitoring function that raises an error."""
        @monitor_function()
        def divide(a: int, b: int) -> float:
            if b == 0:
                raise ValueError("Division by zero")
            return a / b
        
        result = divide(10, 0)
        
        assert isinstance(result, dict)
        assert result["status"] == "error"
        assert result["result"] is None
        assert len(result["errors"]) > 0
        assert "Division by zero" in str(result["errors"])
    
    def test_input_validation_success(self):
        """Test successful input validation."""
        @monitor_function(validate_input=True)
        def process_user(user: TestUser) -> str:
            return f"Hello {user.name}"
        
        user = TestUser(name="John", age=30)
        result = process_user(user)
        
        assert result["status"] == "success"
        assert result["result"] == "Hello John"
    
    def test_input_validation_failure(self):
        """Test input validation failure."""
        @monitor_function(validate_input=True)
        def process_user(user: TestUser) -> str:
            return f"Hello {user.name}"
        
        # This should work since we're passing the right type
        user = TestUser(name="John", age=30)
        result = process_user(user)
        assert result["status"] == "success"
    
    def test_disable_monitoring_features(self):
        """Test disabling various monitoring features."""
        @monitor_function(
            validate_input=False,
            validate_output=False,
            log_execution=False
        )
        def simple_function(x: int) -> int:
            return x * 2
        
        result = simple_function(5)
        assert result["status"] == "success"
        assert result["result"] == 10
    
    def test_execution_timing(self):
        """Test that execution time is measured."""
        @monitor_function()
        def slow_function():
            time.sleep(0.1)
            return "done"
        
        result = slow_function()
        assert result["execution_time"] >= 0.1
    
    @patch('psutil.Process')
    def test_memory_monitoring_disabled(self, mock_process):
        """Test behavior when memory monitoring fails."""
        mock_process.side_effect = Exception("Process monitoring unavailable")
        
        monitor = FunctionMonitor(enable_memory_monitoring=True)
        
        @monitor
        def test_func():
            return "test"
        
        result = test_func()
        assert result["status"] == "success"
        # Memory usage should be zero when monitoring fails
        assert result["memory_usage"]["before"] == 0


class TestFunctionMonitorClass:
    """Test the FunctionMonitor class."""
    
    def test_custom_configuration(self):
        """Test FunctionMonitor with custom configuration."""
        monitor = FunctionMonitor(
            validate_input=False,
            log_execution=False,
            return_raw_result=True
        )
        
        @monitor
        def test_func(x: int) -> int:
            return x + 1
        
        result = test_func(5)
        assert result == 6  # Should return raw result
    
    def test_monitor_reuse(self):
        """Test that monitor instance can be reused."""
        monitor = FunctionMonitor(return_raw_result=True)
        
        @monitor
        def func1(x: int) -> int:
            return x + 1
        
        @monitor
        def func2(x: int) -> int:
            return x * 2
        
        assert func1(5) == 6
        assert func2(5) == 10
