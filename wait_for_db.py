import os
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Maximum number of times to retry the connection
MAX_RETRIES = 15
# Delay in seconds between retries
RETRY_DELAY = 2

# Get DATABASE_URL from environment variable
DB_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:newpassword@postgres:5432/taskdb')

def wait_for_db():
    """
    Waits for the database to become available by repeatedly attempting a connection.
    Exits with code 1 if the connection cannot be established after max retries.
    """
    engine = None
    
    # Try creating the engine, which might fail if DB_URL is invalid
    try:
        engine = create_engine(DB_URL)
    except Exception as e:
        print(f"Error creating database engine with URL {DB_URL}: {e}")
        return False

    # Hide password in log output for security
    safe_url = DB_URL.replace(DB_URL.split('//')[1].split('@')[0], 'user:***')
    print(f"Attempting to connect to database at: {safe_url}")
    
    for i in range(MAX_RETRIES):
        try:
            # Simply try to connect - no need to execute SQL
            connection = engine.connect()
            connection.close()  # Close the connection immediately
            print("Database connection successful. Proceeding with migrations.")
            return True
        except OperationalError as e:
            print(f"Database not yet available (Attempt {i+1}/{MAX_RETRIES}): {str(e)[:100]}...")
            print(f"Waiting {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"An unexpected error occurred during database connection: {e}")
            print(f"Waiting {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)

    print(f"FATAL: Database connection failed after {MAX_RETRIES} attempts.")
    return False

if __name__ == "__main__":
    if not wait_for_db():
        exit(1)