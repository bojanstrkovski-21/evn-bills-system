from functools import wraps

from flask import jsonify, session


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Не сте најавени'}), 401
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Не сте најавени'}), 401
        if session.get('role') != 'admin':
            return jsonify({'error': 'Само администратор може да го направи ова'}), 403
        return view(*args, **kwargs)
    return wrapped
