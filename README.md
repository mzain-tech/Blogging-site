# 📝 Django Blogging Site

## 📌 Project Overview
This is a feature-rich blogging web application built with the Django framework.  
It allows users to create, manage, and share blog posts, organize them into categories, and interact through comments.  

## 📸 Screenshots

### 1️⃣ Admin Dashboard in Website
![Admin Dashboard](assets/admin_dashboard.png)

### 2️⃣ Admin
![Admin](assets/admin.png)

### 3️⃣ Home Page
![Home Page](assets/home_page.png)

### 4️⃣ Login Page
![Login Page](assets/login_page.png)

### 5️⃣ Registration Page
![Registration Page](assets/registration_page.png)

### 6️⃣ Analytics
![Analytics](assets/analytics.png)

## ⚙️ Prerequisites
- Python 3.9 or higher  
- Django (latest stable release recommended)  
- pip (Python package manager)  
- Virtual environment tool (e.g., venv or conda)  

## 🚀 Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/mzain-tech/Blogging-site.git
cd Blogging-site

# 2. Create and activate a virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create a superuser
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver

# 7. Open the project in your browser
http://127.0.0.1:8000/
