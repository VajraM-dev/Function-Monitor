# PyFuncMonitor
[![Documentation](https://img.shields.io/badge/Documentation-8A2BE2)](https://vajram-dev.github.io/pyfuncmonitor-docs/)

A Python decorator for comprehensive function monitoring with execution timing, memory usage tracking, CPU monitoring, input/output validation, and structured logging.

## Features

- **Execution Monitoring**: Track function execution time, memory usage, and CPU utilization
- **Input/Output Validation**: Automatic validation using Pydantic models and type hints
- **Structured Logging**: Configurable structured logging with support for file output
- **Error Handling**: Comprehensive exception handling and error reporting
- **Flexible Configuration**: Global and per-function configuration options
- **Production Ready**: Designed for production use with proper error handling and performance considerations

## Installation

```bash
pip install pyfuncmonitor
```

## Quick Start

```python
from pyfuncmonitor import monitor_function

@monitor_function()
def add_numbers(a: int, b: int) -> int:
    return a + b

result = add_numbers(5, 3)
print(result)
```

This will output a dictionary containing the function result, execution metrics, and monitoring data:

```python
{
    'result': 8,
    'status': 'success',
    'errors': None,
    'execution_time': 0.0001,
    'memory_usage': {
        'before': 15728640,
        'after': 15728640,
        'peak': 15728640,
        'delta': 0
    },
    'cpu_usage': 0.0,
    'timestamp': '2024-01-15T10:30:45.123456',
    'function_name': 'add_numbers'
}
```

## Configuration

### Global Configuration

Configure the monitor globally for your application:

```python
from pyfuncmonitor import configure_monitor

configure_monitor(
    log_to_file=True,
    log_file_path="./app_monitor.log",
    log_level=20,  # INFO level
    default_return_raw_result=True
)
```

### Environment Variables

You can also configure using environment variables:

```bash
export PYFUNCMONITOR_LOG_LEVEL=10  # DEBUG level
export PYFUNCMONITOR_LOG_TO_FILE=true
export PYFUNCMONITOR_LOG_FILE=./debug.log
```

### Per-Function Configuration

Override global settings for specific functions:

```python
@monitor_function(
    validate_input=True,
    validate_output=False,
    log_level="DEBUG",
    return_raw_result=True
)
def my_function(x: int) -> str:
    return str(x * 2)
```

## Advanced Usage

### Input/Output Validation with Pydantic

```python
from pydantic import BaseModel
from pyfuncmonitor import monitor_function

class User(BaseModel):
    name: str
    age: int
    email: str

class UserResponse(BaseModel):
    user: User
    message: str

@monitor_function(validate_input=True, validate_output=True)
def create_user(user_data: User) -> UserResponse:
    return UserResponse(
        user=user_data,
        message=f"User {user_data.name} created successfully"
    )

# Usage
user = User(name="John Doe", age=30, email="john@example.com")
result = create_user(user)
```

### Custom Monitor Instances

```python
from pyfuncmonitor import FunctionMonitor

# Create custom monitor with specific settings
production_monitor = FunctionMonitor(
    validate_input=True,
    validate_output=True,
    log_execution=True,
    return_raw_result=True
)

debug_monitor = FunctionMonitor(
    validate_input=True,
    validate_output=False,
    log_level="DEBUG",
    return_raw_result=False
)

@production_monitor
def critical_function(data: dict) -> dict:
    # Process critical data
    return {"processed": True}

@debug_monitor
def experimental_function(x: int) -> int:
    # Experimental code
    return x ** 2
```

### Error Handling

The monitor automatically captures and reports errors:

```python
@monitor_function()
def divide_numbers(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

result = divide_numbers(10, 0)
print(result["status"])  # "error"
print(result["errors"])  # List of error messages
```

### Memory and CPU Monitoring

Monitor resource usage:

```python
@monitor_function(
    enable_memory_monitoring=True,
    enable_cpu_monitoring=True
)
def memory_intensive_function(size: int) -> list:
    # Create a large list
    return list(range(size))

result = memory_intensive_function(1000000)
print(result["memory_usage"])  # Memory usage statistics
print(result["cpu_usage"])     # CPU usage percentage
```

## Configuration Options

### Global Configuration Parameters

- `log_level`: Logging level (default: INFO)
- `log_to_file`: Enable file logging (default: False)
- `log_file_path`: Path to log file (default: "./pyfuncmonitor.log")
- `log_file_max_size`: Maximum log file size in bytes (default: 10MB)
- `log_file_backup_count`: Number of backup log files (default: 5)
- `default_validate_input`: Default input validation setting (default: True)
- `default_validate_output`: Default output validation setting (default: True)
- `default_log_execution`: Default execution logging setting (default: True)
- `default_return_raw_result`: Default return format setting (default: False)
- `enable_memory_monitoring`: Enable memory monitoring (default: True)
- `enable_cpu_monitoring`: Enable CPU monitoring (default: True)

### Decorator Parameters

- `validate_input`: Enable input validation using type hints
- `validate_output`: Enable output validation using type hints
- `log_execution`: Enable structured logging
- `log_level`: Log level for the function ("DEBUG", "INFO", "WARNING", "ERROR")
- `return_raw_result`: Return original result on success, structured format on error
- `enable_memory_monitoring`: Enable memory usage monitoring
- `enable_cpu_monitoring`: Enable CPU usage monitoring

## Logging

The monitor uses structured logging with configurable output formats:

### Console Logging (Development)
```python
configure_monitor(log_to_file=False)  # Logs to console with readable format
```

### File Logging (Production)
```python
configure_monitor(
    log_to_file=True,
    log_file_path="/var/log/myapp/monitor.log"
)  # Logs to file in JSON format
```

### Custom Log Levels
```python
@monitor_function(log_level="DEBUG")
def debug_function():
    pass

@monitor_function(log_level="ERROR")  # Only log errors
def critical_function():
    pass
```

## Best Practices

1. **Production Usage**: Use `return_raw_result=True` in production to avoid overhead
2. **Input Validation**: Enable input validation for external-facing functions
3. **Log File Management**: Configure log rotation to prevent disk space issues
4. **Selective Monitoring**: Disable CPU/memory monitoring for high-frequency functions if needed
5. **Error Handling**: Always handle the case where monitoring might return error status

```python
# Production configuration example
configure_monitor(
    log_to_file=True,
    log_file_path="/var/log/myapp/pyfuncmonitor.log",
    log_level=20,  # INFO
    default_return_raw_result=True,
    default_validate_input=True,
    default_validate_output=False  # Disable output validation for performance
)

@monitor_function()
def api_endpoint(request_data: RequestModel) -> ResponseModel:
    # Your business logic here
    return process_request(request_data)

# Usage with error handling
result = api_endpoint(request)
if isinstance(result, dict) and result.get("status") == "error":
    # Handle error case
    logger.error("Function failed", errors=result["errors"])
    return error_response()
else:
    # Success case - result is the actual return value
    return result
```

## Performance Considerations

- **Minimal Overhead**: The monitor is designed to have minimal impact on function performance
- **Selective Monitoring**: Disable features you don't need for better performance
- **Memory Monitoring**: Uses `psutil` for accurate memory measurements
- **CPU Monitoring**: Lightweight CPU usage tracking
- **Logging**: Structured logging with configurable levels to reduce I/O overhead

## Error Handling and Debugging

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Permission Issues**: Check file permissions for log files
3. **Memory Monitoring**: Requires `psutil` package
4. **Type Validation**: Requires proper type hints for validation to work

### Debug Mode

Enable debug mode for detailed logging:

```python
from pyfuncmonitor import configure_monitor

configure_monitor(
    log_level=10,  # DEBUG level
    log_to_file=True,
    log_file_path="./debug.log"
)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/VajraM-dev/pyfuncmonitor/issues)
- **PyPI**: [PyPI Package](https://pypi.org/project/pyfuncmonitor/)