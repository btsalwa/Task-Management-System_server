import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'default_url')
    ENVIRONMENT = os.getenv('APP_ENV', 'development')
    
