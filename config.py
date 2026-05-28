import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    PORT = int(os.getenv('PORT', 5000))
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # AI Model Configuration
    AI_MODEL = 'gpt-3.5-turbo'
    AI_TEMPERATURE = 0.7
    AI_MAX_TOKENS = 2000

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
