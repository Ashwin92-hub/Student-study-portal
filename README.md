# Student-study-portal


---

## 📘 Student Utility Hub – Django Web Application

A comprehensive **Django-based web application** designed to help students manage their daily academic tasks efficiently. This platform integrates multiple tools like note-taking, homework tracking, dictionary search, YouTube learning, and more into a single interface.

---

## 🚀 Features

* 📝 **Notes Management**

  * Create, view, and manage notes
  * Detailed note view (`notes_detail.html`)

* ✅ **To-Do List**

  * Track daily tasks (`todo.html`)

* 📚 **Book Search**

  * Find books easily (`books.html`)

* 📖 **Dictionary Tool**

  * Search meanings and definitions (`dictionary.html`)

* 🎥 **YouTube Learning**

  * Search educational videos (`youtube.html`)

* 🌐 **Wikipedia Search**

  * Fetch quick information (`wiki.html`)

* 🔢 **Unit Conversion**

  * Perform conversions (`conversion.html`)

* 📘 **Homework Tracker**

  * Manage assignments (`homework.html`)

* 👤 **User Authentication**

  * Register, Login, Logout
  * User profile management (`profile.html`)

---

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS (Templates)
* **Database:** SQLite (`db.sqlite3`)
* **Authentication:** Django built-in auth system

---

## 📂 Project Structure (Key Files)

* `models.py` – Database schema
* `views.py` – Application logic
* `urls.py` – Routing configuration
* `forms.py` – Form handling
* `templates/` – HTML pages (UI)
* `static/` – CSS & assets (if added)

---

## ⚙️ Installation & Setup

```bash
# Clone the repository
git clone https://github.com/your-username/student-utility-hub.git

# Navigate into the project
cd student-utility-hub

# Create virtual environment
python -m venv env

# Activate environment
env\Scripts\activate  # Windows
source env/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

---

## 🎯 Use Case

This project is ideal for:

* Students managing daily academic tasks
* Beginners learning Django full-stack development
* Mini-project or final-year project implementation

---

## 📌 Future Enhancements

* Mobile responsiveness improvements
* AI-based recommendations (study content)
* Cloud deployment (AWS / Heroku)

---


