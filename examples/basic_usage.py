# examples/basic_usage.py
"""Basic usage examples for function-monitor."""

from function_monitor import monitor_function, configure_monitor
from pydantic import BaseModel
from typing import List 

# Configure the monitor globally
configure_monitor(
    log_to_file=True,
    log_file_path="./function_monitor.log"
)


# Example 1: Basic monitoring
@monitor_function()
def add_numbers(a: int, b: int) -> int:
    """Simple addition function."""
    return a + b


# Example 2: With Pydantic models
class User(BaseModel):
    name: str
    age: int
    email: str


class UserResponse(BaseModel):
    user: User
    message: str


@monitor_function(return_raw_result=True)
def create_user(user_data: User) -> UserResponse:
    """Create a user and return response."""
    return UserResponse(
        user=user_data,
        message=f"User {user_data.name} created successfully"
    )


# Example 3: Function that might fail
@monitor_function(log_level="DEBUG")
def divide_numbers(a: float, b: float) -> float:
    """Division function that might raise an error."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


# Example 4: Function with complex processing
@monitor_function(validate_input=True, validate_output=False)
def process_data(data: List[int], multiplier: int = 2) -> List[int]:
    """Process a list of numbers."""
    import time
    # Simulate some processing time
    time.sleep(0.1)
    return [x * multiplier for x in data]


if __name__ == "__main__":
    # Test basic function
    print("=== Basic Addition ===")
    result = add_numbers(5, 3)
    print(f"Result: {result}")
    
    # Test with Pydantic models
    print("\n=== User Creation ===")
    user = User(name="John Doe", age=30, email="john@example.com")
    response = create_user(user)
    print(f"Response: {response}")
    
    # Test division (success case)
    print("\n=== Division Success ===")
    division_result = divide_numbers(10.0, 2.0)
    print(f"Division result: {division_result}")
    
    # Test division (error case)
    print("\n=== Division Error ===")
    try:
        error_result = divide_numbers(10.0, 0.0)
    except:
        pass  # Error will be logged
    
    # Test data processing
    print("\n=== Data Processing ===")
    processed = process_data([1, 2, 3, 4, 5], multiplier=3)
    print(f"Processed data: {processed}")