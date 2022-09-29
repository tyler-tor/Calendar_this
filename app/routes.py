import sqlite3
from flask import (Blueprint, render_template, redirect)
from app.forms import AppointmentForm
import os
from datetime import datetime

bp = Blueprint('main', __name__, url_prefix='/')
DB_FILE = os.environ.get("DB_FILE")


@bp.route('/', methods=['GET', 'POST'])
def main():
    form = AppointmentForm()
    if form.validate_on_submit():
        params = (
            form.name.data,
            datetime.combine(form.start_date.data, form.start_time.data),
            datetime.combine(form.end_date.data, form.end_time.data),
            form.description.data,
            form.private.data
        )
        with sqlite3.connect(DB_FILE) as conn:
            curs = conn.cursor()
            curs.execute('''
            INSERT INTO appointments
            (name, start_datetime, end_datetime, description, private)
            VALUES
            (?,?,?,?,?)
            ''', params)
            return redirect("/", code=302)
    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute('''
            select id, name, start_datetime, end_datetime
            from appointments
            order by start_datetime;
        ''')
        rows = curs.fetchall()
        # datetime_obj = datetime.strptime(rows['start_time'], '%Y-%m-%d %H:%M:%S')
        # print(datetime_obj)
        for row in rows:
            print(row)
    return render_template('main.html', rows=rows, datetime=datetime, form=form)
