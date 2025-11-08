from flask import Blueprint, render_template, jsonify
from app.models import Program, Document, RequirementSet, University, Country
from ..extenisions import db
import requests
from bs4 import BeautifulSoup

import_bp = Blueprint("import", __name__, url_prefix="/import-program-api")

@import_bp.route("/api/v1/import-program", methods=['POST'])
def import_program(url):
    page_content = requests.get(url).text
    