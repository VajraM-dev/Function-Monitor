# tests/test_models.py
"""Tests for Pydantic models."""

from function_monitor.models import ExecutionResult, MemoryUsage


class TestMemoryUsage:
    """Test MemoryUsage model."""
    
    def test_memory_usage_creation(self):
        """Test creating MemoryUsage model."""
        memory = MemoryUsage(
            before=1000,
            after=1500,
            peak=1600,
            delta=500
        )
        
        assert memory.before == 1000
        assert memory.after == 1500
        assert memory.peak == 1600
        assert memory.delta == 500


class TestExecutionResult:
    """Test ExecutionResult model."""
    
    def test_create_success(self):
        """Test creating successful execution result."""
        memory_usage = {
            "before": 1000,
            "after": 1500,
            "peak": 1600,
            "delta": 500
        }
        
        result = ExecutionResult.create_success(
            result="test result",
            execution_time=0.1,
            memory_usage=memory_usage,
            cpu_usage=15.5,
            function_name="test_func"
        )
        
        assert result.status == "success"
        assert result.result == "test result"
        assert result.execution_time == 0.1
        assert result.cpu_usage == 15.5
        assert result.function_name == "test_func"
        assert result.errors is None
        assert isinstance(result.memory_usage, MemoryUsage)
    
    def test_create_error(self):
        """Test creating error execution result."""
        memory_usage = {
            "before": 1000,
            "after": 1000,
            "peak": 1000,
            "delta": 0
        }
        
        errors = ["Error message 1", "Error message 2"]
        
        result = ExecutionResult.create_error(
            errors=errors,
            execution_time=0.05,
            memory_usage=memory_usage,
            cpu_usage=10.0,
            function_name="failing_func"
        )
        
        assert result.status == "error"
        assert result.errors == errors
        assert result.execution_time == 0.05
        assert result.function_name == "failing_func"
    
    def test_model_dump(self):
        """Test model serialization."""
        memory_usage = {
            "before": 1000,
            "after": 1500,
            "peak": 1600,
            "delta": 500
        }
        
        result = ExecutionResult.create_success(
            result={"key": "value"},
            execution_time=0.1,
            memory_usage=memory_usage,
            cpu_usage=15.5,
            function_name="test_func"
        )
        
        dumped = result.model_dump()
        
        assert isinstance(dumped, dict)
        assert dumped["status"] == "success"
        assert dumped["result"] == {"key": "value"}
        assert "timestamp" in dumped
        assert isinstance(dumped["memory_usage"], dict)