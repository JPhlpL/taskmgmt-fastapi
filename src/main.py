from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import contacts
from src.utils.logger import setup_logfire

web_app = FastAPI()

setup_logfire(web_app)

# Set up CORS with your allowed origins
# origins = [
#     "http://localhost:3000",
#     "http://10.73.130.177:3000",
#     "http://10.74.12.26:3000",
#     "http://172.24.68.121:3000"
# ]

web_app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the user router (and any additional routers)
web_app.include_router(contacts.router)
