import pymysql
import os
from dotenv import load_dotenv

# 상위 디렉토리의 config 폴더에서 .env 파일 로드
dotenv_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config', '.env'))
load_dotenv(dotenv_path=dotenv_path)



# 데이터베이스 생성 테스트 함수
def test_create_database():
    # 환경 변수에서 DB 정보 가져오기
    db_host = "localhost"
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

    # MySQL 연결 시도
    try:
        connection = pymysql.connect(host=db_host, user=db_user, password=db_password, port=db_port)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        connection.commit()
        cursor.close()
        connection.close()
        assert True  # 데이터베이스 생성이 성공하면 테스트 통과
    except Exception as e:
        assert False, f"Error creating database: {e}"
