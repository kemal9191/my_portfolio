from flask import render_template, request, Blueprint
from sqlalchemy import null
from app.models import *
from app import db
from app.models import Content

main = Blueprint('main', __name__)


@main.route('/home')
@main.route('/')
def home():
    return render_template('main/home.html')


@main.route('/projects')
def projects():
    page = request.args.get('page', 1, type=int)
    projects = Content.query.filter_by(type='Project').order_by(Content.date_added.desc())\
        .paginate(page=page, per_page=3)
    return render_template('main/projects.html', projects=projects)


@main.route('/articles')
def articles():
    flask = db.session.query(Content).filter(Content.subjects.contains({'Flask'})).count()
    javascript = db.session.query(Content).filter(Content.subjects.contains({'JavaScript'})).count()
    css = db.session.query(Content).filter(Content.subjects.contains({'CSS3'})).count()
    bootstrap = db.session.query(Content).filter(Content.subjects.contains({'Bootstrap'})).count()
    HTML = db.session.query(Content).filter(Content.subjects.contains({'HTML5'})).count()
    python = db.session.query(Content).filter(Content.subjects.contains({'Python'})).count()
    categories = {'Flask': flask, 'JavaScript': javascript, 'CSS3': css, 'Bootstrap': bootstrap, 'HTML5': HTML, 'Python': python}
    page = request.args.get('page', 1, type=int)
    articles = Content.query.filter_by(type='Article').order_by(Content.date_added.desc())\
        .paginate(page=page, per_page=3)
    return render_template('main/articles.html', articles=articles, categories=categories)


@main.route('/projects/<int:id>')
def project_detailed(id):
    project = Content.query.filter_by(type='Project', id=id).one_or_none()
    return render_template('main/item-details.html', content=project)


@main.route('/articles/<int:id>')
def article_detailed(id):
    article = Content.query.filter_by(type='Article', id=id).one_or_none()
    return render_template('main/item-details.html', content=article)


@main.route('/contact')
def contact():
    return render_template('main/contact.html')