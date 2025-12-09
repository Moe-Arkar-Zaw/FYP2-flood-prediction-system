import os 
from dotenv import load_dotenv 

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Mysql
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    # Directories
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
    FRAME_FOLDER = os.getenv("FRAME_FOLDER")
    MODEL_FOLDER = os.getenv("MODEL_FOLDER")

    # Upload limits
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 200 * 1024 * 1024))