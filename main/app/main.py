from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import authentication,aacount_details,password_route,profile_pic
from .models import user_models
from .database import database

app = FastAPI(
    title="An Attendance Management System website api\ ",
    description="""This is starting now""",
)


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello to the attendance management system"}


#creating the tables
user_models.database.Base.metadata.create_all(bind=database.engine)



#including all the routers 
app.include_router(authentication.router)
app.include_router(aacount_details.router)
app.include_router(password_route.router)
app.include_router(profile_pic.router)