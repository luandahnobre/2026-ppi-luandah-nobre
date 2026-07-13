from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from blog_news.auth import login_required
from blog_news.db import get_db

bp = Blueprint('news', __name__)


@bp.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT n.id, n.title, n.content, n.image, n.created_at, n.user_id, u.name'
        ' FROM news n JOIN users u ON n.user_id = u.id'
        ' ORDER BY n.created_at DESC'
    )
    noticias = cursor.fetchall()
    return render_template('news/index.html', noticias=noticias)


def get_noticia(id, check_author=True):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT n.id, n.title, n.content, n.image, n.created_at, n.user_id, u.name'
        ' FROM news n JOIN users u ON n.user_id = u.id'
        ' WHERE n.id = %s',
        (id,)
    )
    noticia = cursor.fetchone()

    if noticia is None:
        from werkzeug.exceptions import abort
        abort(404)

    if check_author and noticia['user_id'] != g.user['id']:
        from werkzeug.exceptions import abort
        abort(403)

    return noticia


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        image = request.form['image'].strip()
        error = None

        if not title:
            error = 'Título é obrigatório.'
        elif not content:
            error = 'Conteúdo é obrigatório.'
        elif not image:
            error = 'URL da imagem é obrigatória.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO news (title, content, image, user_id) VALUES (%s, %s, %s, %s)',
                (title, content, image, g.user['id'])
            )
            db.commit()
            return redirect(url_for('news.index'))

    return render_template('news/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    noticia = get_noticia(id)

    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        image = request.form['image'].strip()
        error = None

        if not title:
            error = 'Título é obrigatório.'
        elif not content:
            error = 'Conteúdo é obrigatório.'
        elif not image:
            error = 'URL da imagem é obrigatória.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'UPDATE news SET title = %s, content = %s, image = %s WHERE id = %s',
                (title, content, image, id)
            )
            db.commit()
            return redirect(url_for('news.index'))

    return render_template('news/update.html', noticia=noticia)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_noticia(id)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM news WHERE id = %s', (id,))
    db.commit()
    return redirect(url_for('news.index'))
