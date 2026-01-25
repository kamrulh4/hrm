# HRM System

A comprehensive Human Resource Management (HRM) System built with a multi-tenant architecture, featuring a robust Django backend and a modern Next.js frontend.

## 🚀 Features

- **Multi-tenant Architecture**: Support for multiple organizations with isolated data.
- **Subscription Management**: Tiered subscription plans for organizations.
- **Advanced User Management**: Custom user roles, JWT authentication, and OTP-based verification.
- **Background Tasks**: Asynchronous processing using Celery and Redis.
- **Mikrotik Integration**: Built-in support for Mikrotik network management.
- **Modern Admin UI**: Beautiful and functional dashboard using Django Unfold.
- **API Documentation**: Interactive documentation powered by Swagger/OpenAPI.

## 🛠 Tech Stack

- **Backend**: [Django 5.2](https://www.djangoproject.com/), [Django REST Framework](https://www.django-rest-framework.org/)
- **Frontend**: [Next.js](https://nextjs.org/)
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Task Queue**: [Celery](https://docs.celeryq.dev/) with [Redis](https://redis.io/)
- **Web Server**: [Nginx](https://www.nginx.com/)
- **Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

## 🏁 Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system.

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hrm
   ```

2. **Configure Environment Variables**:
   Copy the example environment file and update it with your settings:
   ```bash
   cp dot.env.example.txt .env
   ```

3. **Spin up the services**:
   ```bash
   docker-compose up --build
   ```

### 📍 Access Points

- **Frontend**: [http://localhost](http://localhost)
- **Backend API**: [http://localhost/api/v1](http://localhost/api/v1)
- **Admin Panel**: [http://localhost/admin](http://localhost/admin)
- **Swagger Documentation**: [http://localhost/api/docs](http://localhost/api/docs)

## 🔧 Development

### Backend (Local Setup)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements/dev.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```

## 🧹 Utilities

The project includes a cleanup script for Docker:
```bash
./docker-cleanup.sh
```

---
Built with ❤️ for efficient HR management.
