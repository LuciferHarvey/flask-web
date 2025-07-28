# Flask Blog Application

Ứng dụng blog được xây dựng bằng Flask với đầy đủ tính năng quản lý người dùng và bài viết.
<->
## Tính năng

### Người dùng
- ✅ Đăng ký tài khoản mới
- ✅ Đăng nhập/Đăng xuất
- ✅ Xem blog của người khác
- ✅ Tạo/Sửa/Xóa bài viết của chính mình

### Admin
- ✅ Trang quản trị với dashboard
- ✅ Quản lý tất cả người dùng
- ✅ Quản lý tất cả bài viết
- ✅ Thống kê hệ thống

### Giao diện
- ✅ Bootstrap 5 responsive design
- ✅ Icons với Bootstrap Icons
- ✅ Mobile-friendly interface
- ✅ Modern card-based layout

### Công nghệ
- ✅ Flask web framework
- ✅ MongoDB database
- ✅ Docker Compose containerization
- ✅ Flask-Login authentication
- ✅ bcrypt password hashing

## Cài đặt và Chạy

### Với Docker Compose (Khuyến nghị)

```bash
# Clone hoặc tải project
cd flask-web

# Chạy với Docker Compose
docker-compose up --build

# Truy cập ứng dụng tại http://localhost:5000
```

### Chạy Local

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy MongoDB (cần cài đặt trước)
mongod

# Chạy ứng dụng
python app.py

# Truy cập tại http://localhost:5000
```

## Tài khoản Demo

**Admin Account:**
- Username: `admin`
- Password: `admin123`

## Cấu trúc Project

```
flask-web/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker Compose config
├── Dockerfile            # Docker container config
├── .env                  # Environment variables
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── create_post.html  # Create post
│   ├── edit_post.html    # Edit post
│   ├── view_post.html    # View post
│   ├── my_posts.html     # User's posts
│   └── admin.html        # Admin panel
└── .github/
    └── copilot-instructions.md
```

## Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  username: String,
  email: String,
  password: String (hashed),
  is_admin: Boolean,
  created_at: Date
}
```

### Posts Collection
```javascript
{
  _id: ObjectId,
  title: String,
  content: String,
  author_id: ObjectId,
  created_at: Date,
  updated_at: Date
}
```

## Environment Variables

```env
MONGODB_URI=mongodb://localhost:27017/flask_blog
SECRET_KEY=your-very-secret-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=True
```

## API Routes

- `GET /` - Trang chủ với danh sách bài viết
- `GET/POST /register` - Đăng ký tài khoản
- `GET/POST /login` - Đăng nhập
- `GET /logout` - Đăng xuất
- `GET/POST /create_post` - Tạo bài viết mới
- `GET /post/<id>` - Xem bài viết
- `GET/POST /edit_post/<id>` - Chỉnh sửa bài viết  
- `GET /delete_post/<id>` - Xóa bài viết
- `GET /my_posts` - Bài viết của người dùng
- `GET /admin` - Trang quản trị
- `GET /admin/delete_user/<id>` - Xóa người dùng (admin)

## Screenshots

### Trang chủ
- Hiển thị danh sách bài viết mới nhất
- Sidebar với thông tin và thống kê
- Navigation bar với menu người dùng

### Trang Admin
- Tab quản lý người dùng và bài viết
- Thống kê tổng quan hệ thống
- Các hành động CRUD đầy đủ

### Responsive Design
- Hoạt động tốt trên mobile và desktop
- Bootstrap responsive grid system
- Touch-friendly interface

## Phát triển thêm

Một số tính năng có thể thêm vào:
- Comment system cho bài viết
- Like/Unlike posts
- User profiles với avatar
- Email verification
- Password reset
- Rich text editor
- Image upload
- Search functionality
- Pagination
- Categories/Tags
- Social login

## License

MIT License - Tự do sử dụng cho mục đích học tập và thương mại.
