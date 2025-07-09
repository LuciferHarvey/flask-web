from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# MongoDB setup
client = MongoClient(app.config['MONGODB_URI'])
db = client.get_default_database()
users_collection = db.users
posts_collection = db.posts

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        self.is_admin = user_data.get('is_admin', False)

@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

# Routes
@app.route('/')
def index():
    posts = list(posts_collection.find().sort('created_at', -1))
    for post in posts:
        author = users_collection.find_one({'_id': post['author_id']})
        post['author_name'] = author['username'] if author else 'Unknown'
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        if users_collection.find_one({'$or': [{'username': username}, {'email': email}]}):
            flash('Tên người dùng hoặc email đã tồn tại!')
            return render_template('register.html')
        
        # Create new user
        hashed_password = generate_password_hash(password)
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'is_admin': False,
            'created_at': datetime.now()
        }
        
        result = users_collection.insert_one(user_data)
        flash('Đăng ký thành công! Vui lòng đăng nhập.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user_data = users_collection.find_one({'username': username})
        
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            flash('Đăng nhập thành công!')
            return redirect(url_for('index'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đã đăng xuất thành công!')
    return redirect(url_for('index'))

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        post_data = {
            'title': title,
            'content': content,
            'author_id': ObjectId(current_user.id),
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        posts_collection.insert_one(post_data)
        flash('Bài viết đã được tạo thành công!')
        return redirect(url_for('index'))
    
    return render_template('create_post.html')

@app.route('/post/<post_id>')
def view_post(post_id):
    post = posts_collection.find_one({'_id': ObjectId(post_id)})
    if not post:
        flash('Bài viết không tồn tại!')
        return redirect(url_for('index'))
    
    author = users_collection.find_one({'_id': post['author_id']})
    post['author_name'] = author['username'] if author else 'Unknown'
    
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = posts_collection.find_one({'_id': ObjectId(post_id)})
    
    if not post:
        flash('Bài viết không tồn tại!')
        return redirect(url_for('index'))
    
    if str(post['author_id']) != current_user.id and not current_user.is_admin:
        flash('Bạn không có quyền chỉnh sửa bài viết này!')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        posts_collection.update_one(
            {'_id': ObjectId(post_id)},
            {'$set': {
                'title': title,
                'content': content,
                'updated_at': datetime.now()
            }}
        )
        
        flash('Bài viết đã được cập nhật!')
        return redirect(url_for('view_post', post_id=post_id))
    
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<post_id>')
@login_required
def delete_post(post_id):
    post = posts_collection.find_one({'_id': ObjectId(post_id)})
    
    if not post:
        flash('Bài viết không tồn tại!')
        return redirect(url_for('index'))
    
    if str(post['author_id']) != current_user.id and not current_user.is_admin:
        flash('Bạn không có quyền xóa bài viết này!')
        return redirect(url_for('index'))
    
    posts_collection.delete_one({'_id': ObjectId(post_id)})
    flash('Bài viết đã được xóa!')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang quản trị!')
        return redirect(url_for('index'))
    
    users = list(users_collection.find())
    posts = list(posts_collection.find().sort('created_at', -1))
    
    for post in posts:
        author = users_collection.find_one({'_id': post['author_id']})
        post['author_name'] = author['username'] if author else 'Unknown'
    
    return render_template('admin.html', users=users, posts=posts)

@app.route('/admin/delete_user/<user_id>')
@login_required
def admin_delete_user(user_id):
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập!')
        return redirect(url_for('index'))
    
    # Don't allow admin to delete themselves
    if user_id == current_user.id:
        flash('Bạn không thể xóa tài khoản của chính mình!')
        return redirect(url_for('admin_panel'))
    
    users_collection.delete_one({'_id': ObjectId(user_id)})
    posts_collection.delete_many({'author_id': ObjectId(user_id)})
    flash('Người dùng và tất cả bài viết của họ đã được xóa!')
    return redirect(url_for('admin_panel'))

@app.route('/my_posts')
@login_required
def my_posts():
    posts = list(posts_collection.find({'author_id': ObjectId(current_user.id)}).sort('created_at', -1))
    return render_template('my_posts.html', posts=posts)

if __name__ == '__main__':
    # Create admin user if doesn't exist
    admin_user = users_collection.find_one({'username': 'admin'})
    if not admin_user:
        admin_data = {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': generate_password_hash('admin123'),
            'is_admin': True,
            'created_at': datetime.now()
        }
        users_collection.insert_one(admin_data)
        print('Admin user created: username=admin, password=admin123')
    
    app.run(host='0.0.0.0', port=80, debug=True)
