from flask import redirect, flash, jsonify, render_template, Blueprint, request, url_for
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import Admin, Content
from app.admin.forms import LoginForm, ContentForm
from app.admin.utils import save_picture


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
    return render_template('admin/login.html', form=form, title="login")


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout is successful', 'success')
    return redirect(url_for('admin.login'))


@admin.route('/admin/projects')
@login_required
def all_projects():
    page = request.args.get('page', 1, type=int)
    projects = Content.query.filter_by(type='Project').order_by(Content.date_added.desc())\
        .paginate(page=page, per_page=30)
    return render_template('admin/projects.html', projects=projects, title="projects")


@admin.route('/admin/articles')
@login_required
def all_articles():
    flask = db.session.query(Content).filter_by(type='Article').filter(Content.subjects.contains({'Flask'})).count()
    javascript = db.session.query(Content).filter_by(type='Article').filter(Content.subjects.contains({'JavaScript'})).count()
    css = db.session.query(Content).filter_by(type='Article').filter(Content.subjects.contains({'CSS3'})).count()
    bootstrap = db.session.query(Content).filter_by(type='Article').filter(Content.subjects.contains({'Bootstrap'})).count()
    HTML = db.session.query(Content).filter_by(type='Article').filter(Content.subjects.contains({'HTML5'})).count()
    python = db.session.query(Content).filter_by(type='Article').filter(Content.subjects.contains({'Python'})).count()
    categories = {'Flask': flask, 'JavaScript': javascript, 'CSS3': css, 'Bootstrap': bootstrap, 'HTML5': HTML, 'Python': python}
    page = request.args.get('page', 1, type=int)
    articles = Content.query.filter_by(type='Article').order_by(Content.date_added.desc())\
        .paginate(page=page, per_page=30)
    total = Content.query.filter_by(type='Article').count()
    return render_template('admin/articles.html', articles=articles, categories=categories, total=total, title="articles")


@admin.route('/admin/articles/<string:category>')
@login_required
def show_by_category(category):
    flask = db.session.query(Content).filter_by(type='Article').filter(Content.subjects.contains({'Flask'})).count()
    javascript = db.session.query(Content).filter_by(type='Article').filter(Content.subjects.contains({'JavaScript'})).count()
    css = db.session.query(Content).filter_by(type='Article').filter(Content.subjects.contains({'CSS3'})).count()
    bootstrap = db.session.query(Content).filter_by(type='Article').filter(Content.subjects.contains({'Bootstrap'})).count()
    HTML = db.session.query(Content).filter_by(type='Article').filter(Content.subjects.contains({'HTML5'})).count()
    python = db.session.query(Content).filter_by(type='Article').filter(Content.subjects.contains({'Python'})).count()
    categories = {'Flask': flask, 'JavaScript': javascript, 'CSS3': css, 'Bootstrap': bootstrap, 'HTML5': HTML, 'Python': python}
    page = request.args.get('page', 1, type=int)
    articles = Content.query.filter_by(type='Article').filter(Content.subjects.contains({category})).order_by(Content.date_added.desc())\
        .paginate(page=page, per_page=30)
    total = Content.query.filter_by(type='Article').count()
    return render_template('admin/articles.html', articles=articles, categories=categories, total=total, title="articles", category=category)


@admin.route('/admin/update/<int:id>', methods=['GET','POST'])
@login_required
def update_content(id):
    form = ContentForm()
    content = Content.query.get(id)
    if request.method == 'GET':
        form.type.data = content.type
        form.subjects.data = content.subjects
        form.title.data = content.title
        form.content.data = content.content
        form.image.data = content.image
        if content.type=="Article":
            title = "articles"
        if content.type=="Project":
            title = "projects"
    if request.method == 'POST':
        if form.validate_on_submit:
            if form.image.data:
                image = save_picture(form.image.data)
                url = url_for('static', filename="images/"+image)
                content.image = url
            content.type = form.type.data
            content.subjects = form.subjects.data
            content.title = form.title.data
            content.content = form.content.data
            db.session.commit()
            flash("Content has been updated!", "success")
            title = form.type.data
        else:
            flash("Please check your input!")
            return redirect(url_for('admin.update_content'))
        if content.type == 'Article':
            return redirect(url_for('admin.all_articles'))
        if content.type == 'Project':
            return redirect(url_for('admin.all_projects'))
    return render_template('admin/admin.html', form=form, title=title)


@admin.route('/admin/delete/<int:id>', methods=['GET','DELETE'])
@login_required
def delete_content(id):
    content = Content.query.get(id)
    db.session.delete(content)
    db.session.commit()
    flash('Content has been deleted!', "info")
    return redirect(url_for('admin.all_projects'))
    

@admin.route('/admin/new', methods=['POST', 'GET'])
@login_required
def add_content():
    form = ContentForm()
    if form.validate_on_submit():
        if form.image.data:
            image = save_picture(form.image.data)
            url = url_for('static', filename="images/"+image)
            content = Content(type=form.type.data, title=form.title.data,
                            subjects=form.subjects.data, content=form.content.data,
                            image=url, admin=current_user)
        else:
            content = Content(type=form.type.data, title=form.title.data,
                                subjects=form.subjects.data, content=form.content.data,
                                image='', admin=current_user)
        db.session.add(content)
        db.session.commit()
        flash('Your content has been created!', 'success')
        return redirect(url_for('admin.add_content'))
    return render_template('admin/admin.html', form=form, title="add")