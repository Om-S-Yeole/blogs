# Blog Platform - README

## Project Overview
This is a **Blog Platform** built using Django and PostgreSQL. It allows users to read, like and comment on blog posts created by superuser while providing an intuitive interface for users and administrators. The platform is designed to grow with advanced features like user authentication, tagging, and a search system. The project can also be scaled further to include APIs, real-time updates, and modern frontend integrations.

---

## Features

### Current Features:
- User authentication (login, registration, logout)
- Create, read, update, and delete blog posts (CRUD functionality)
- Tagging system for organizing posts
- Responsive design using Bootstrap
- Admin interface for managing posts and users

### Future Features:
- Advanced search functionality
- Rich text editor for post creation
- User roles (e.g., admin, editor, reader)
- Real-time notifications
- API integration (REST or GraphQL)

---

## Technologies Used

### Backend:
- Django: Python web framework
- PostgreSQL: Relational database

### Frontend:
- HTML, CSS, JavaScript
- Bootstrap: For responsive design

### Deployment:
- Docker (future integration)
- Nginx and Gunicorn (production setup)

---

## Installation

### Prerequisites:
- Python 3.x
- PostgreSQL

### Steps to Install:
1. Clone the repository:
   ```bash
   git clone https://github.com/Om-S-Yeole/Blog_Website.git
   cd Blog_Website
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:
   ```sql
   CREATE DATABASE blogdb;
   CREATE USER bloguser WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE blogdb TO bloguser;
   ```

5. Update `settings.py` with your database configuration:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'blogdb',
           'USER': 'bloguser',
           'PASSWORD': 'password',
           'HOST': 'localhost',
           'PORT': '',
       }
   }
   ```

6. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Create a superuser for the admin interface:
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

9. Open the app in your browser:
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Usage

1. **Admin Interface:**
   - Access the admin panel at `/admin` to manage users and posts.

2. **Public Interface:**
   - Users can browse, read, and search for posts.
---

## Folder Structure
```
myblog/
|-- blog/               # Main application folder
|   |-- migrations/     # Database migrations
|   |-- templates/      # HTML templates
|   |-- static/         # Static files (CSS, JS, images)
|   |-- views.py        # Views for the blog
|   |-- models.py       # Database models
|-- myblog/             # Project settings folder
|   |-- settings.py     # Django settings
|   |-- urls.py         # URL configuration
|-- manage.py           # Django management script
```

---

## Future Enhancements
- Implement full-text search
- Add API endpoints using Django REST Framework
- Deploy the application using Docker, Nginx, and Gunicorn
- Add multi-language support (internationalization)
- Integrate with cloud storage (e.g., AWS S3) for media files

---

**Start Blogging Today! 🚀**
