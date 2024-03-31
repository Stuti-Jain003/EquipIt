from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from sqlalchemy import func, or_
from sqlalchemy.orm import backref
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwerty'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///category.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post_category.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post_database.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comment_database.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reply_database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

categories = ["Washing Machine", "Oven", "Mobile", "Refrigerator", "Microwave", "Toaster", "Other"]


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    # posts = db.relationship('Post', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    

class PostCategory(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    video_link = db.Column(db.String(255), nullable=True)
    instructions = db.Column(db.Text, nullable=False)
    equipment_link = db.Column(db.String(255), nullable=True)
    maps_link = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    categories = db.relationship('Category', secondary='post_category', backref=db.backref('posts', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # likes = db.Column(db.Integer, default=0)
    # dislikes = db.Column(db.Integer, default=0)
    
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('replies', lazy=True))
    comment = db.relationship('Comment', backref=db.backref('replies', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create the database tables
with app.app_context():
    # db.drop_all() 
    db.create_all()


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/login', methods=['GET'])
def show_login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            print(current_user)
            return redirect(url_for('home'))

        return 'Invalid email or password. Please try again.'

    return render_template('login.html')


@app.route('/account')
@login_required
def account():
    print(current_user)
    return render_template('account.html', current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    
    # Flash a message for the user
    flash('You have been logged out successfully.', 'success')

    # Redirect to the home page after logout
    return redirect(url_for('home'))


@app.route('/home')
def home():
    # messages = flash.get_flashed_messages()

    # Render the home page with flash messages
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return 'Email is already registered. Please choose another email.'

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('signup.html')


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        title = request.form['title']
        video_link = request.form['video_link']
        instructions = request.form['instructions']
        equipment_link = request.form['equipment_link']
        maps_link = request.form['maps_link']
        category_name = request.form['category']

        new_post = Post(
            title=title,
            video_link=video_link,
            instructions=instructions,
            equipment_link=equipment_link,
            maps_link=maps_link,
            author=current_user
        )
        
        category_name = request.form['category']
        
        selected_category = Category.query.filter_by(name=category_name).first()  
        if not selected_category:
            selected_category = Category(name=category_name)      
        
        if selected_category is not None:
            new_post.categories.append(selected_category)
            db.session.add(new_post)
            db.session.commit()
        else:
    # Handle the case where the category is not found or is None
           flash('Invalid category. Please select a valid category.', 'error')
    # Redirect or render the form again with an error message
           return redirect(url_for('post', categories=categories))
        
        db.session.add(new_post)
        db.session.commit()

        # Redirect to the page showing the actual post
        return redirect(url_for('view_post', post_id=new_post.id))

    return render_template('post.html', categories=categories)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view_post.html', post=post)


@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('term', '')
    
    # Get a list of selected categories from the query parameters
    categories = request.args.getlist('category')

    # Query based on post title and category names
    search_results = (
        Post.query.filter(Post.title.ilike(f'%{search_term}%'))
        .outerjoin(Post.categories)
        .filter(or_(*[Category.name.ilike(f'%{category}%') for category in categories]))
        .group_by(Post.id)
        .order_by(func.count().desc())
        .all()
    )

    return render_template('search_results.html', search_results=search_results)


@app.route('/add_comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    if request.method == 'POST':
        comment_text = request.form['comment_text']
        post = Post.query.get_or_404(post_id)

        new_comment = Comment(text=comment_text, user=current_user)
        post.comments.append(new_comment)
        db.session.commit()

    return redirect(url_for('view_post', post_id=post_id))


@app.route('/add_reply/<int:comment_id>', methods=['POST'])
@login_required
def add_reply(comment_id):
    if request.method == 'POST':
        reply_text = request.form['reply_text']
        comment = Comment.query.get_or_404(comment_id)

        new_reply = Reply(text=reply_text, user=current_user)
        comment.replies.append(new_reply)
        db.session.commit()

    return redirect(request.referrer)
    
    
# @app.route('/like_post/<int:post_id>', methods=['POST'])
# @login_required
# def like_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     post.likes += 1
#     db.session.commit()
#     return redirect(url_for('view_post', post_id=post_id))


# @app.route('/dislike_post/<int:post_id>', methods=['POST'])
# @login_required
# def dislike_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     post.dislikes += 1
#     db.session.commit()
#     return redirect(url_for('view_post', post_id=post_id))


if __name__ == '__main__':
    app.run(debug=True)
