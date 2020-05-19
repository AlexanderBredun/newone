from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from app.main.forms import SimpleForm, EditProfileForm, PostForm, SearchForm
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime
from flask_babel import _, get_locale
from guess_language import guess_language
from app.translate import translate, detect
from app.main import bp
from app.search import add_to_index, remove_from_index, query_index


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    


    g.locale = str(get_locale())
    
    

@bp.route('/', methods = ['post', 'get'])
@bp.route('/index', methods = ['post', 'get'])
@login_required
def index():
    form = PostForm()

    if form.validate_on_submit():
        language = detect(form.post.data)
        print(language)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''

        posts = Post(body = form.post.data, author = current_user, language = language)
        db.session.add(posts)
        
        db.session.commit()

        flash(_('Ur post succsesfully published'))

        return redirect(url_for('main.index'))



    

    page = request.args.get('page', 1, type = int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )

    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None

    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
        

    return render_template('index.html',
        title = _('yo title'),
        posts = posts.items,
        user = current_user,
        form = form,
        prev_url = prev_url,
        next_url = next_url)



@bp.route('/settings', methods = ['GET', 'POST'])
@login_required
def settings():
    form = SimpleForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).update(dict(theme2 = str(request.form['example'])))
        db.session.commit()
        print(form.example.data)
        flash(_('Settings saved succesfully'))
        return redirect(url_for('main.index'))
    
    return render_template('settings.html',form=form,user = current_user)


@bp.route('/user/<username>')
@login_required

def user(username):
    user = User.query.filter_by(username = username).first_or_404()

    page = request.args.get('page', 1, type = int)

    posts = Post.query.filter_by(author = user).order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )

    next_url = url_for('main.user', username = user.username, page=posts.next_num) \
        if posts.has_next else None

    prev_url = url_for('main.user', username = user.username, page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('user.html',
    title = _('My home broski'),
    user = user,
    posts = posts.items,
    prev_url = prev_url,
    next_url = next_url)

@bp.route('/edit_profile', methods = ['post', 'get'])

def edit_profile():

    form = EditProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Changes saved succesfully!'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form = form)

@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        flash(_('user %(username)s not found', username = username))
        return redirect(url_for('main.index'))

    if user == current_user:
        flash(_('u cannot follow yourself'))

    current_user.follow(user)
    db.session.commit()
    flash(_('u are following %(username)s now', username = username))

    return redirect(url_for('main.user', username = username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        flash(_('user %(username)s not found', username = username))
        return redirect(url_for('main.index'))

    if user == current_user:
        flash(_('u cannot unfollow yourself'))

    current_user.unfollow(user)
    db.session.commit()
    flash(_('u are not following %(username)s now', username = username))

    return redirect(url_for('main.user', username = username))


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type = int)
    
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None

    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template("index.html", title='Explore', posts=posts.items,
                          next_url=next_url, prev_url=prev_url)




@bp.route('/translate', methods = ['post'])
@login_required
def translate_text():
    print(request.form['text'])
    return jsonify({'text' : translate(request.form['text'], request.form['dest_language'])})


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None

    print(total)
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url, total = total)


