# examples/configuration_examples.py
"""Configuration examples for function-monitor."""

import os
from function_monitor import configure_monitor, monitor_function, MonitorConfig


def example_environment_based_config():
    """Configure based on environment variables."""
    
    # Set environment variables (in practice, these would be set externally)
    os.environ["FUNCTION_MONITOR_LOG_LEVEL"] = "10"  # DEBUG level
    os.environ["FUNCTION_MONITOR_LOG_TO_FILE"] = "true"
    os.environ["FUNCTION_MONITOR_LOG_FILE"] = "./debug.log"
    
    # The configuration will automatically pick up these environment variables
    config = MonitorConfig.from_env()
    print(f"Config from env: {config}")


def example_programmatic_config():
    """Configure programmatically."""
    
    configure_monitor(
        log_level=20,  # INFO level
        log_to_file=True,
        log_file_path="./app_monitor.log",
        default_validate_input=True,
        default_validate_output=False,
        default_return_raw_result=True
    )


def example_custom_config():
    """Create and use custom configuration."""
    
    custom_config = MonitorConfig(
        log_level=10,  # DEBUG
        log_to_file=True,
        log_file_path="./custom_monitor.log",
        default_validate_input=True,
        default_validate_output=True,
        enable_memory_monitoring=True,
        enable_cpu_monitoring=False  # Disable CPU monitoring
    )
    
    # Apply the custom configuration
    from function_monitor import set_config
    set_config(custom_config)


@monitor_function()
def test_function(x: int) -> int:
    """Test function to demonstrate configuration effects."""
    return x * 2


if __name__ == "__main__":
    print("=== Environment-based Configuration ===")
    example_environment_based_config()
    result1 = test_function(5)
    print(f"Result 1: {result1}")
    
    print("\n=== Programmatic Configuration ===")
    example_programmatic_config()
    result2 = test_function(10)
    print(f"Result 2: {result2}")
    
    print("\n=== Custom Configuration ===")
    example_custom_config()
    result3 = test_function(15)
    print(f"Result 3: {result3}")