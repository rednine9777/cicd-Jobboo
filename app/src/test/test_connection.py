import pymysql
import os
from dotenv import load_dotenv

# Calculate the path to the .env file and load it
dotenv_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config', '.env'))
print("Attempting to load .env from:", dotenv_path)
if os.path.exists(dotenv_path):
    print(".env file exists")
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(".env file does not exist")

# MySQL connection test function
def test_mysql_connection():
    # Retrieve DB information from environment variables
    db_host = "db"
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
        connection.close()
        assert True  # Test passes if connection is successful
    except Exception as e:
        assert False, f"Error connecting to MySQL: {e}"
