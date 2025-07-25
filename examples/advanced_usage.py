"""Advanced usage examples for function-monitor."""

from function_monitor import monitor_function, configure_monitor, FunctionMonitor
from pydantic import BaseModel, validator
from typing import Optional, Dict, Any
import asyncio


# Custom configuration for different environments
def setup_production_config():
    """Setup configuration for production environment."""
    configure_monitor(
        log_to_file=True,
        log_file_path="/var/log/myapp/function_monitor.log",
        default_log_level="INFO",
        default_return_raw_result=True
    )


def setup_development_config():
    """Setup configuration for development environment."""
    configure_monitor(
        log_to_file=False,  # Log to console only
        default_log_level="DEBUG",
        default_return_raw_result=False  # Return full monitoring data
    )


# Custom monitor instances with different configurations
production_monitor = FunctionMonitor(
    validate_input=True,
    validate_output=True,
    log_execution=True,
    return_raw_result=True
)

debug_monitor = FunctionMonitor(
    validate_input=True,
    validate_output=False,
    log_execution=True,
    log_level="DEBUG",
    return_raw_result=False
)


# Complex Pydantic models
class DatabaseConfig(BaseModel):
    host: str
    port: int
    database: str
    username: str
    password: str
    
    @validator('port')
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v


class QueryResult(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    rows_affected: int = 0


# Example with database-like operations
@production_monitor
def connect_to_database(config: DatabaseConfig) -> str:
    """Simulate database connection."""
    # Simulate connection logic
    import time
    time.sleep(0.05)  # Simulate connection time
    return f"Connected to {config.database} at {config.host}:{config.port}"


@debug_monitor
def execute_query(query: str, params: Optional[Dict[str, Any]] = None) -> QueryResult:
    """Simulate query execution."""
    import time
    import random
    
    # Simulate query processing time
    time.sleep(random.uniform(0.01, 0.1))
    
    # Simulate occasional failures
    if random.random() < 0.1:  # 10% failure rate
        return QueryResult(
            success=False,
            error_message="Simulated database error",
            rows_affected=0
        )
    
    # Simulate successful query
    return QueryResult(
        success=True,
        data={"result": "Query executed successfully"},
        rows_affected=random.randint(1, 100)
    )


# Example with retry logic
@monitor_function(log_level="DEBUG")
def api_call_with_retry(url: str, max_retries: int = 3) -> Dict[str, Any]:
    """Simulate API call with retry logic."""
    import time
    import random
    
    for attempt in range(max_retries):
        try:
            # Simulate API call
            time.sleep(0.1)
            
            # Simulate occasional failures
            if random.random() < 0.3:  # 30% failure rate
                raise ConnectionError(f"API call failed (attempt {attempt + 1})")
            
            return {
                "status": "success",
                "data": f"Response from {url}",
                "attempt": attempt + 1
            }
            
        except ConnectionError as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(0.5 * (attempt + 1))  # Exponential backoff


# Example with async function (note: monitoring works with sync functions)
@monitor_function()
def async_wrapper(coro_func, *args, **kwargs):
    """Wrapper to monitor async functions."""
    return asyncio.run(coro_func(*args, **kwargs))


async def async_operation(duration: float) -> str:
    """Example async operation."""
    await asyncio.sleep(duration)
    return f"Async operation completed after {duration} seconds"


# Example with class methods
class DataProcessor:
    """Example class with monitored methods."""
    
    def __init__(self, name: str):
        self.name = name
    
    @monitor_function(return_raw_result=True)
    def process_batch(self, batch_size: int, data: list) -> Dict[str, Any]:
        """Process data in batches."""
        import time
        
        processed_items = 0
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            time.sleep(0.01)  # Simulate processing time
            processed_items += len(batch)
        
        return {
            "processor": self.name,
            "total_items": len(data),
            "processed_items": processed_items,
            "batch_size": batch_size
        }
    
    @staticmethod
    @monitor_function()
    def validate_data(data: list) -> bool:
        """Static method to validate data."""
        return all(isinstance(item, (int, float, str)) for item in data)


if __name__ == "__main__":
    # Setup development configuration
    setup_development_config()
    
    # Test database operations
    print("=== Database Operations ===")
    db_config = DatabaseConfig(
        host="localhost",
        port=5432,
        database="testdb",
        username="user",
        password="pass"
    )
    
    connection = connect_to_database(db_config)
    print(f"Connection: {connection}")
    
    # Test query execution
    query_result = execute_query("SELECT * FROM users", {"limit": 10})
    print(f"Query result: {query_result}")
    
    # Test API call with retry
    print("\n=== API Call with Retry ===")
    try:
        api_result = api_call_with_retry("https://api.example.com/data")
        print(f"API result: {api_result}")
    except Exception as e:
        print(f"API call failed: {e}")
    
    # Test async wrapper
    print("\n=== Async Operation ===")
    async_result = async_wrapper(async_operation, 0.1)
    print(f"Async result: {async_result}")
    
    # Test class methods
    print("\n=== Class Methods ===")
    processor = DataProcessor("BatchProcessor-1")
    test_data = list(range(100))
    
    is_valid = DataProcessor.validate_data(test_data)
    print(f"Data validation: {is_valid}")
    
    processing_result = processor.process_batch(10, test_data)
    print(f"Processing result: {processing_result}")