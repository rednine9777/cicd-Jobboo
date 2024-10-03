# test_database.py

import pymysql
import os
from dotenv import load_dotenv

# 환경에 따라 .env 파일 경로를 동적으로 설정
dotenv_path = "/app/.env"
load_dotenv(dotenv_path=dotenv_path)

# Database existence check function
def test_database_exists():
    # 환경 변수에서 DB 정보 가져오기
    db_host = os.getenv('MYSQL_HOST', 'db')  # 기본값으로 'db' 설정
    db_user = os.getenv('MYSQL_USER')
    db_password = os.getenv('MYSQL_PASSWORD')
    db_port = int(os.getenv('MYSQL_PORT', 3306))
    db_name = os.getenv('MYSQL_DATABASE')

    # 환경 변수가 제대로 로드됐는지 출력
    print("Loaded MYSQL_USER:", db_user)
    print("Loaded MYSQL_PASSWORD:", db_password)
    print("Loaded MYSQL_DATABASE:", db_name)
    print("Loaded MYSQL_HOST:", db_host)
    print("Loaded MYSQL_PORT:", db_port)

    # MySQL에 연결하여 데이터베이스가 존재하는지 확인
    try:
        connection = pymysql.connect(host=db_host, user=db_user, password=db_password, port=db_port)
        cursor = connection.cursor()

        # 데이터베이스가 존재하는지 확인
        cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
        result = cursor.fetchone()

        if result:
            print(f"Database {db_name} exists.")
            assert True  # 데이터베이스가 존재하면 테스트 통과
        else:
            print(f"Database {db_name} does not exist.")
            assert False, "Database does not exist."  # 데이터베이스가 존재하지 않으면 테스트 실패

        cursor.close()
        connection.close()

    except Exception as e:
        assert False, f"Error checking database existence: {e}"
        print(f"Error checking database existence: {e}")
