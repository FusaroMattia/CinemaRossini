from flask import Blueprint, render_template, redirect, url_for, request,flash
from flask_login import login_user, logout_user, login_required,current_user
from . import db
from sqlalchemy import create_engine, text
import sqlite3

main = Blueprint('main', __name__)
conn = sqlite3.connect('rossini.db', check_same_thread=False)
cursor = conn.cursor()

@main.route('/')
def index():
    query = "SELECT * FROM proiezioni  ORDER BY data  DESC, ora DESC"
    cursor.execute(query)
    results = cursor.fetchmany(4)
    cursor.close()
    return render_template('index.html', results = results)

@main.route('/profile')
def profile():
    if current_user.is_authenticated :
        return render_template('profile.html', name=current_user.name)
    else:
        return render_template('profile.html')
