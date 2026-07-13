import os
import pymysql
from flask import g


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', ''),
            database=os.environ.get('DB_NAME', 'blog_news'),
            port=int(os.environ.get('DB_PORT', 3306)),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r') as f:
        sql = f.read()
    cursor = db.cursor()
    for statement in sql.split(';'):
        statement = statement.strip()
        if statement:
            cursor.execute(statement)
    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
