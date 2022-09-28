import sqlite3
from flask import (Blueprint, render_template)
import os


bp = Blueprint('main', __name__, url_prefix='/')
DB_FILE = os.environ.get("DB_FILE")


@bp.route('/')
def main():
    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute('select * from appointments;')
        rows = curs.fetchall()
        print(rows[0][2])
    return render_template('main.html', rows=rows)
