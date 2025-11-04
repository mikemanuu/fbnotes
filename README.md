
---

# 📘 fbnotes

*fbnotes* is a bookmarking and note-taking web application built to help users save and annotate Facebook posts.  
It lets you capture posts, add notes, tag them, and even attach media for context — all stored securely in your personal database.

This app is ideal for researchers, content creators, and social media managers who want a private and organized way to manage Facebook content.

---

## ✨ Key Features

- Save and categorize Facebook posts you want to revisit  
- Add custom notes to posts for context or insights  
- Tag bookmarks with multiple tags for quick filtering  
- Upload related screenshots or files  
- View audit logs for every action taken  
- Simple, responsive Bootstrap interface  
- RESTful API for browser extensions or mobile integration  
- Dockerized for easy deployment and scalability  

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|-------------|
| *Frontend* | HTML, CSS, JavaScript, Bootstrap |
| *Backend* | Django Framework (Python) |
| *Database* | MySQL |
| *API* | Django REST Framework |
| *Server & Deployment* | Docker, Gunicorn, Nginx |
| *Version Control* | Git & GitHub |

---

## 🧩 System Architecture Overview

### 1. *Frontend (Client Layer)*
The frontend is built with *HTML, CSS, JS, and Bootstrap*.  
It communicates with the backend via RESTful APIs using AJAX or Fetch requests.

*Responsibilities:*
- Render user interface and forms (login, dashboard, bookmark view, note editor)
- Send CRUD requests to the API endpoints
- Display responses dynamically

---

### 2. *Backend (Application Layer)*

Powered by *Django* and *Django REST Framework*, this layer handles:
- Business logic (creating, editing, deleting bookmarks and notes)
- User authentication and authorization
- API endpoint exposure for third-party tools (like a browser extension)
- Media and file uploads
- Logging all user actions in the AuditLog model

---

### 3. *Database (Persistence Layer)*

The *MySQL* database stores all persistent data, including:
- User accounts and credentials
- Bookmarks and their metadata
- Notes and tags
- Uploaded media
- System audit logs

Below is a simplified *database schema* representation:

+------------------+ |      User        | +------------------+ | id (PK)          | | username         | | email            | | password         | | date_joined      | +------------------+

+------------------+ |     Bookmark     | +------------------+ | id (PK)          | | user_id (FK)     | | post_url         | | post_title       | | date_saved       | | is_favorite      | +------------------+

+------------------+ |      Note        | +------------------+ | id (PK)          | | bookmark_id (FK) | | content          | | created_at       | | updated_at       | +------------------+

+------------------+ |       Tag        | +------------------+ | id (PK)          | | name             | +------------------+

+------------------+ |   BookmarkTag    | +------------------+ | id (PK)          | | bookmark_id (FK) | | tag_id (FK)      | +------------------+

+------------------+ |      Media       | +------------------+ | id (PK)          | | bookmark_id (FK) | | file_path        | | uploaded_at      | +------------------+

+------------------+ |    AuditLog      | +------------------+ | id (PK)          | | user_id (FK)     | | action           | | timestamp        | | ip_address       | +------------------+

---

## 🧭 API Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| /api/bookmarks/ | GET, POST | Fetch or create bookmarks |
| /api/bookmarks/<id>/ | GET, PUT, DELETE | Retrieve, update, or delete bookmark |
| /api/notes/ | GET, POST | Manage user notes |
| /api/tags/ | GET, POST | Manage tags |
| /api/media/ | GET, POST | Upload and fetch media |
| /api/auditlogs/ | GET | View all logged actions |
| /api/auth/login/ | POST | Authenticate user |
| /api/auth/register/ | POST | Create new account |

All endpoints use *JWT (JSON Web Token)* authentication for secure access.

---

## ⚙ Setup and Installation

### 1. *Clone the repository*
```bash
git clone https://github.com/mikemanuu/fbnotes.git
cd fbnotes
```
### 2. *Create environment variables*
```
Copy .env.example to .env and fill in:

MYSQL_DB=fbnotes_db
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_HOST=db
SECRET_KEY=your_django_secret
DEBUG=True
```

### 3. *Run Docker containers*
```
docker-compose build
docker-compose up -d
```
### 4. *Apply database migrations*
```
docker-compose exec web python manage.py migrate
```
### 5. *Create superuser*
```
docker-compose exec web python manage.py createsuperuser
```
### 6. *Access the app*
```
Visit http://localhost to open the web interface.
```

---

## 🧠 How It Works
```
1. User logs in or registers
The authentication system validates credentials and returns a JWT token.


2. User saves a Facebook post
The frontend sends the post link and metadata to the /api/bookmarks/ endpoint.


3. Notes and Tags added
Notes are attached to a bookmark, and multiple tags can be applied for organization.


4. Media uploaded
Screenshots or files are uploaded via /api/media/ and linked to the bookmark.


5. Audit logging
Every change (create, update, delete) is recorded automatically in AuditLog.

```


---

## 🏗 Architecture Diagram (Text Version)
```
[Browser Extension / Web UI]
          |
          v
   [Django REST API]
          |
          v
       [MySQL DB]

```
---

## 🧪 Testing
```
To run tests inside Docker:

docker-compose exec web python manage.py test

```
---

## 🔒 Security Practices
```
Environment variables stored in .env

CSRF protection enabled

JWT-based authentication

Validation for file uploads

HTTPS recommended in production

```

---

## 📦 Deployment (Production)
```
Use the provided Docker Compose configuration:

docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

This runs:

Django app via Gunicorn

MySQL database

Nginx as a reverse proxy

```

---

## 📄 License
```
Licensed under the MIT License © 2025 Emmanuel Rotich
```

---

## 👨‍💻 Developer
```
Name: Emmanuel Rotich

Socials	Link

<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/x.svg" width="20"/> X (Twitter)	twitter.com/yourhandle
<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/linkedin.svg" width="20"/> LinkedIn	linkedin.com/in/yourprofile
<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/github.svg" width="20"/> GitHub	github.com/yourusername
<img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/facebook.svg" width="20"/> Facebook	facebook.com/yourprofile
📧 Email	yourname@email.com

```

---
```
Built with passion, persistence, and Python 🐍
```
---
