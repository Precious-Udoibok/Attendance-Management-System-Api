import os
from dotenv import load_dotenv

load_dotenv()

DATABASEURL = os.getenv("DB_URL")
