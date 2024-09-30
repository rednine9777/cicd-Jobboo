import pymysql
import os
from dotenv import load_dotenv

# Load the .env file
dotenv_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config', '.env'))
load_dotenv(dotenv_path=dotenv_path)

# Database creation test function
def test_create_database():
    # Fetch DB information from environment variables
    db_host = "db"  # Change to 'db' for Docker container
    db_user = os.getenv('MYSQL_USER')
    db_password = os.getenv('MYSQL_PASSWORD')
    db_port = int(os.getenv('MYSQL_PORT', 3306))
    db_name = os.getenv('MYSQL_DATABASE')

    # Print loaded environment variables
    print("Loaded MYSQL_USER:", db_user)
    print("Loaded MYSQL_PASSWORD:", db_password)
    print("Loaded MYSQL_DATABASE:", db_name)
    print("Loaded MYSQL_HOST:", db_host)
    print("Loaded MYSQL_PORT:", db_port)

    # Attempt to connect to MySQL
    try:
        connection = pymysql.connect(host=db_host, user=db_user, password=db_password, port=db_port)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        connection.commit()
        cursor.close()
        connection.close()
        assert True  # Test passes if DB creation is successful
    except Exception as e:
        assert False, f"Error creating database: {e}"
