"""
This file imports all models in the correct dependency order
so that Flask-Migrate (Alembic) can build the tables correctly.

Order:
1. Tables with no dependencies (Country, Document, User)
2. Tables that depend on them (University, BlogPost)
3. Tables that depend on those (Program)
4. Tables that depend on Program (RequirementSet, Bookmark)
"""

# Level 0: No dependencies
from .user import User
from .university import Country
from .requirement import Document

# Level 1: Depend on Level 0
from .university import University  # Depends on Country
from .blogpost import BlogPost      # Depends on User

# Level 2: Depend on Level 1
from .programs import Program        # Depends on University

# Level 3: Depend on Level 2
from .requirement import RequirementSet # Depends on Program, Document
from .bookmark import Bookmark      # Depends on User, Program