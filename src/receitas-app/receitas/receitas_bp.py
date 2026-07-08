from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from receitas.auth import login_required
from receitas.db import get_db

bp = Blueprint('receitas', __name__)


@bp.route('/')
def index():
    db = get_db()
    lista = db.execute(
        'SELECT r.id, titulo, ingredientes, modo_preparo, tempo_preparo,'
        ' categoria, created, author_id, username'
        ' FROM receita r JOIN user u ON r.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('receitas/index.html', receitas=lista)


def get_receita(id, check_author=True):
    receita = get_db().execute(
        'SELECT r.id, titulo, ingredientes, modo_preparo, tempo_preparo,'
        ' categoria, created, author_id, username'
        ' FROM receita r JOIN user u ON r.author_id = u.id'
        ' WHERE r.id = ?',
        (id,)
    ).fetchone()

    if receita is None:
        abort(404, f"Receita id {id} não existe.")

    if check_author and receita['author_id'] != g.user['id']:
        abort(403)

    return receita


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        titulo = request.form['titulo'].strip()
        ingredientes = request.form['ingredientes'].strip()
        modo_preparo = request.form['modo_preparo'].strip()
        tempo_preparo = request.form.get('tempo_preparo', 0, type=int)
        categoria = request.form.get('categoria', 'outros').strip()
        error = None

        if not titulo:
            error = 'Título é obrigatório.'
        elif not ingredientes:
            error = 'Ingredientes são obrigatórios.'
        elif not modo_preparo:
            error = 'Modo de preparo é obrigatório.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO receita (titulo, ingredientes, modo_preparo,'
                ' tempo_preparo, categoria, author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (titulo, ingredientes, modo_preparo, tempo_preparo,
                 categoria, g.user['id'])
            )
            db.commit()
            return redirect(url_for('receitas.index'))

    return render_template('receitas/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    receita = get_receita(id)

    if request.method == 'POST':
        titulo = request.form['titulo'].strip()
        ingredientes = request.form['ingredientes'].strip()
        modo_preparo = request.form['modo_preparo'].strip()
        tempo_preparo = request.form.get('tempo_preparo', 0, type=int)
        categoria = request.form.get('categoria', 'outros').strip()
        error = None

        if not titulo:
            error = 'Título é obrigatório.'
        elif not ingredientes:
            error = 'Ingredientes são obrigatórios.'
        elif not modo_preparo:
            error = 'Modo de preparo é obrigatório.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE receita SET titulo = ?, ingredientes = ?,'
                ' modo_preparo = ?, tempo_preparo = ?, categoria = ?'
                ' WHERE id = ?',
                (titulo, ingredientes, modo_preparo, tempo_preparo,
                 categoria, id)
            )
            db.commit()
            return redirect(url_for('receitas.index'))

    return render_template('receitas/update.html', receita=receita)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_receita(id)
    db = get_db()
    db.execute('DELETE FROM receita WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('receitas.index'))
