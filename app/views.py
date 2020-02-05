from app import app , db
from flask import render_template , redirect , flash , url_for ,request
from app.forms import LoginForm , RegistrationForm , EditProfileForm , PostForm
from flask_login import current_user , login_user , logout_user , login_required
from app.models import User , Post
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()


@app.route('/' , methods=['GET' , 'POST'])
@app.route('/home/' , methods=['GET' , 'POST'])
@login_required
def home():

	form = PostForm()

	if form.validate_on_submit() :
		post = Post(body=form.post.data , author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('your post is on live')
		return redirect(url_for('home'))

	user = {'username':"yeswanth"}

	posts = current_user.followed_posts().all()

	return render_template('home.html' , posts=posts, form=form,title='home')




@app.route('/register/' , methods=['POST' , 'GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data , email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template("register.html" , title='Register' , form=form )




@app.route('/login/' ,methods=['POST' , 'GET'])
def login():
	
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid login id or password')
			return redirect(url_for('login'))

		login_user( user , remember=form.remember_me.data)
		#login_user( user , remember=True)

		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '' :
			next_page = url_for('home')
		return redirect(next_page)

	return render_template( 'login.html', title='Sign In' , form=form)


@app.route('/logout/')
def logout():
	logout_user()

	return redirect(url_for('home'))


@app.route('/user/<username>/')
@login_required
def user(username):

	user = User.query.filter_by(username=username).first_or_404()

	posts = Post.query.order_by(Post.timeStamp.desc()).all()

	return render_template("user.html", user=user , posts= posts)

	

@app.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('editprofile.html', title='Edit Profile',
                           form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('home'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('home'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/explore/')
@login_required
def explore():
	posts = Post.query.order_by(Post.timeStamp.desc()).all()

	return render_template('home.html' , posts=posts , title='Explore' )