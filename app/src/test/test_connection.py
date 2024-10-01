import pymysql
import os
from dotenv import load_dotenv

# 환경에 따라 .env 파일 경로를 동적으로 설정
# dotenv_path = os.getenv('DOTENV_PATH')
dotenv_path = "/app/.env"
load_dotenv(dotenv_path=dotenv_path)

# MySQL connection test function
def test_mysql_connection():
    # Retrieve DB information from environment variables
    db_host = os.getenv('MYSQL_HOST', 'db')  # 기본값으로 'db' 설정
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
        print("MySQL connection successful!")
    except Exception as e:
        assert False, f"Error connecting to MySQL: {e}"
        print(f"Error connecting to MySQL: {e}")
