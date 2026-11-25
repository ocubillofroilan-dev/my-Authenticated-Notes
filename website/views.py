from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import db
from .models import Note

views = Blueprint('views', __name__)

MAX_NOTE_LENGTH = 10000


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = (request.form.get('note') or '').strip()

        if not note:
            flash('Note is too short!', category='error')
        elif len(note) > MAX_NOTE_LENGTH:
            flash(f'Note is too long (max {MAX_NOTE_LENGTH} characters).', category='error')
        else:
            db.session.add(Note(data=note, user_id=current_user.id))
            db.session.commit()
            flash('Note added!', category='success')

        # Redirect so refreshing the page doesn't submit the form again.
        return redirect(url_for('views.home'))

    return render_template('home.html')


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    data = request.get_json(silent=True) or {}

    try:
        note_id = int(data.get('noteId'))
    except (TypeError, ValueError):
        return jsonify(error='Invalid note id.'), 400

    note = db.session.get(Note, note_id)
    if note is None:
        return jsonify(error='Note not found.'), 404
    if note.user_id != current_user.id:
        return jsonify(error='Not allowed.'), 403

    db.session.delete(note)
    db.session.commit()
    return jsonify(success=True)