from flask import Blueprint, render_template

error = Blueprint('error', __name__)


@error.app_errorhandler(400)
def error_400(error):
    return render_template('error/400.html'), 400


@error.app_errorhandler(401)
def error_401(error):
    return render_template('error/401.html'), 401


@error.app_errorhandler(403)
def error_403(error):
    return render_template('error/403.html'), 403


@error.app_errorhandler(404)
def error_404(error):
    return render_template('error/404.html'), 404


@error.app_errorhandler(500)
def error_500(error):
    return render_template('error/500.html'), 500
