# Flask Blog Application

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Mô tả dự án
Đây là một ứng dụng blog được xây dựng bằng Flask với các tính năng:

### Tính năng chính:
- **Người dùng**: Đăng ký, đăng nhập, đăng xuất
- **Blog**: Tạo, sửa, xóa, xem bài viết 
- **Admin**: Quản lý người dùng và bài viết
- **UI**: Giao diện Bootstrap responsive
- **Database**: MongoDB với PyMongo
- **Container**: Docker Compose

### Cấu trúc dự án:
- `app.py`: Main Flask application
- `config.py`: Configuration settings
- `templates/`: HTML templates với Bootstrap
- `requirements.txt`: Python dependencies
- `docker-compose.yml`: Container orchestration
- `Dockerfile`: Application container

### Database Collections:
- `users`: Thông tin người dùng, authentication
- `posts`: Bài viết blog với metadata

### Authentication:
- Sử dụng Flask-Login và bcrypt
- Session-based authentication
- Admin role system

### Coding Guidelines:
- Sử dụng Python naming conventions
- Comments bằng tiếng Việt cho business logic
- Bootstrap classes cho styling
- MongoDB ObjectId cho relationships
- Error handling với flash messages
