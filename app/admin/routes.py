from flask import redirect, flash, jsonify, render_template, Blueprint, request, url_for
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import Admin, Content
from app.admin.forms import LoginForm, ContentForm

admin = Blueprint('admin', __name__)


@admin.route('/admin', methods=['GET', 'POST'])
@admin.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.add_content'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(name=form.username.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.add_content'))
        else:
            flash('Login unsuccessful. Please check username or password', 'danger')
    return render_template('admin/login.html', form=form)


@admin.route('/logout')
def logout():
    logout_user()
    flash('Logout is successful', 'success')
    return redirect(url_for('admin.login'))


@admin.route('/admin/projects')
def all_projects():
    page = request.args.get('page', 1, type=int)
    projects = Content.query.filter_by(type='Project').order_by(Content.date_added.desc())\
        .paginate(page=page, per_page=3)
    return render_template('admin/projects.html', projects=projects)


@admin.route('/admin/articles')
def all_articles():
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
    return render_template('admin/articles.html', articles=articles, categories=categories)


@admin.route('/admin/projects/<int:id>', methods=['PATCH'])
def update_project(id):
    return render_template('admin/admin.html')


@admin.route('/admin/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    pass


@admin.route('/admin/articles/<int:id>', methods=['PATCH'])
def update_article(id):
    return render_template('admin/admin.html')


@admin.route('/admin/articles/<int:id>', methods=['DELETE'])
def delete_article(id):
    pass

@admin.route('/admin/new', methods=['POST', 'GET'])
@login_required
def add_content():
    form = ContentForm()
    if form.validate_on_submit():
        content = Content(type=form.type.data, title=form.title.data,
                            subjects=form.subjects.data, content=form.content.data,
                            image='images/home.jpeg', admin=current_user)
        db.session.add(content)
        db.session.commit()
        flash('Your content has been created!', 'success')
        return redirect(url_for('admin.add_content'))
    return render_template('admin/admin.html', form=form)