import os
from dotenv import load_dotenv

load_dotenv()

DATABASEURL = os.getenv("DB_URL")
SECRET_KEY= os.getenv("SECRET_KEY ")
ALGORITHM= os.getenv("ALGORITHM ")