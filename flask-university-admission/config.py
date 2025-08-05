import os

# define the basedir
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Universal Configuration, applied to all environments
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or "this-is-a-secret-key"

class DevConfig:
    """Configuration for Development Environment
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    
    DEBUG = True

class ProdConfig:
    """Configuration for Production environment
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    
    DEBUG = False