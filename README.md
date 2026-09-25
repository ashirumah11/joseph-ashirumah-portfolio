# Modern Full-Stack Software Engineer Portfolio — Django

A production-grade, extensible personal portfolio and case-study platform built for **Joseph Ashirumah**, **Full-Stack Software Engineer**.

Engineered with **Python, Django, SQL, HTML5, CSS3, Bootstrap 5, and Vanilla JavaScript**, this application demonstrates end-to-end full-stack capability: relational database modeling, clean Django architecture, an interactive developer UI, and a content management system powered by Django Admin.

---

## 🌟 Key Features

* **Custom Developer Aesthetic:** Deep charcoal/slate visual theme (`#080c14`), electric cyan and emerald accents, terminal emulator card with simulated Python code and copy-to-clipboard, pulsing status availability indicator.
* **Core Specialization Showcase:** Highlighting **Python • Django • SQL • React** with categorized capability cards (Backend, Database, Frontend, Tools & Engineering). No misleading percentages.
* **Engineering Case Studies:** Dedicated `/projects/<slug>/` architecture breakdowns detailing problem statements, technical resolutions, data modeling, concurrency challenges, and learnings.
* **Filterable Project Archive:** Search bar and technology tag pills for instant client/server filtering across repositories.
* **Interactive Journey Timeline:** Unified vertical timeline displaying work experience, education, certifications, and project milestones.
* **Robust Contact Engine:** Working contact form featuring:
  - Input validation and email sanity checks
  - Invisible honeypot bot trap for spam protection
  - Asynchronous AJAX submission with graceful standard POST fallback
  - Django Messages framework integration
  - Optional SMTP email notifications via environment variables
* **Complete Content Management via Django Admin:** Manage profile, bio, CV upload, avatar, skills, projects, case studies, journey items, social links, and contact inquiries without touching HTML.
* **Production-Ready Architecture:** Environment variable decoupling via `python-dotenv`, PostgreSQL-ready database engine with `dj-database-url`, static asset compression with `whitenoise`, and `gunicorn` WSGI server configuration.
* **Automated Test Suite:** 16 unit tests covering models, slug generation, views, search, filters, forms, and security endpoints.
* **SEO Optimized:** Dynamic `robots.txt`, dynamic `sitemap.xml`, OpenGraph tags, Twitter Card metadata, and semantic HTML5 hierarchy.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3.12, Django 6.0, Django ORM, Django Forms, Django Messages |
| **Database** | SQLite (Local Dev) / PostgreSQL (Production via `dj-database-url`) |
| **Frontend** | HTML5, CSS3 Custom Properties, Bootstrap 5.3, Bootstrap Icons, Vanilla JavaScript (ES6+) |
| **Static & Serving** | WhiteNoise 6.6, Gunicorn 22.0, Python-dotenv |
| **Testing** | Django TestCase & Test Client |

---

## 📂 Project Architecture

```text
joseph-ashirumah-portfolio/
│
├── config/                     # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py             # Modular settings with .env loading & WhiteNoise
│   ├── urls.py                 # Root URL configuration & media routing
│   └── wsgi.py                 # WSGI entrypoint for Gunicorn
│
├── core/                       # Core portfolio application
│   ├── management/commands/
│   │   ├── seed_data.py        # Populates realistic starter content & case studies
│   │   └── create_admin.py     # Creates local development superuser
│   ├── context_processors.py   # Global site context (profile, socials, settings)
│   ├── models.py               # Profile, SkillCategory, Skill, Experience, etc.
│   ├── views.py                # Home, About, Robots.txt, Sitemap.xml
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── projects/                   # Engineering projects and case studies
│   ├── models.py               # Project, ProjectTechnology with auto-slugification
│   ├── views.py                # Filterable project list and case study detail
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── contact/                    # Contact submission and notification system
│   ├── models.py               # ContactMessage model with IP logging
│   ├── forms.py                # ContactForm with honeypot spam guard
│   ├── views.py                # AJAX / standard submission handler
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── static/                     # Static assets
│   ├── css/style.css           # Custom design system & dark developer theme
│   ├── js/main.js              # Navbar scroll, terminal copy, AJAX forms
│   └── images/                 # SVGs (avatar placeholder, architecture diagram)
│
├── templates/                  # Reusable Django templates
│   ├── base.html               # Base layout with SEO, fonts, and scripts
│   ├── home.html               # Landing page (Hero, Skills, Projects, Contact)
│   ├── about.html              # Dedicated biography & engineering philosophy
│   ├── 404.html & 500.html     # Custom styled error pages
│   ├── includes/
│   │   ├── navbar.html         # Responsive navigation with Let's Talk CTA
│   │   ├── footer.html         # Footer with copyright and Django badge
│   │   └── messages.html       # Flash alerts component
│   ├── projects/
│   │   ├── project_list.html   # Search & filterable projects catalog
│   │   └── project_detail.html # Comprehensive engineering case study
│   └── contact/
│       └── contact.html        # Standalone contact page
│
├── media/                      # Uploaded CV files, profile photos, screenshots
├── requirements.txt            # Dependency manifest
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── Procfile                    # Deployment process command for PaaS
├── runtime.txt                 # Target Python runtime
└── manage.py
```

---

## 🚀 Quickstart & Local Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd joseph-ashirumah-portfolio
```

### 2. Set up virtual environment (recommended)
```bash
python -m venv venv

# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(On Windows PowerShell, use `Copy-Item .env.example .env`)*.

### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. Seed starter portfolio content
Populate the database with realistic projects, categorized skills, and profile data:
```bash
python manage.py seed_data
```

### 7. Create developer admin account
Run the automated command to create or update the local superuser:
```bash
python manage.py create_admin
```
* Default credentials:
  - **Username:** `admin`
  - **Password:** `admin12345`
*(Or use standard `python manage.py createsuperuser`)*.

### 8. Start local development server
```bash
python manage.py runserver
```
Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🧪 Running Automated Tests

Run the full test suite across all apps:
```bash
python manage.py test
```

Run tests for an individual app:
```bash
python manage.py test core
python manage.py test projects
python manage.py test contact
```

---

## ⚙️ Content Management Guide (Django Admin)

Access the admin dashboard at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

### 1. Profile & Bio (`/admin/core/profile/`)
* **Personal Identity:** Edit your name, title, eyebrow tag, headline, and bio introduction.
* **Media & Documents:** Upload your headshot photograph (`profile_photo`) and your PDF résumé (`cv_file`).
  > *Note:* The **"Download CV"** button automatically appears on the navbar and hero when a CV file is uploaded.
* **Status Indicator:** Toggle `status_active` and edit `status_badge` (e.g. *"Available for Software Engineering Opportunities"*).
* **Terminal Code Snippet:** Customize the Python snippet rendered in the hero terminal card.

### 2. Software Projects & Case Studies (`/admin/projects/project/`)
* Add your real-world applications or client systems.
* Fill in the structured engineering case study fields:
  - **Problem Statement:** What operational bottleneck or technical challenge existed?
  - **Solution Statement:** How does your application resolve the problem?
  - **Architecture Description:** Technical architecture, database schema, services used.
  - **Key Features:** Bullet points or functional breakdown.
  - **Challenges & Learnings:** Concurrency issues, performance optimizations, trade-offs.
* Assign technology tags and upload architecture diagrams or screenshots.
* Mark projects as **Featured** to highlight them on the homepage.

### 3. Skills & Categories (`/admin/core/skillcategory/` & `/admin/core/skill/`)
* Group technologies into categories (*Backend, Database, Frontend, Tools*).
* Flag skills with `is_primary_stack=True` (e.g., Python, Django, SQL) to highlight them with custom cyan borders and "Primary" badges.

### 4. Experience & Journey (`/admin/core/experience/`)
* Add work positions, education degrees, verified certifications, or major milestones.
* Entries display chronologically in the interactive vertical timeline.

### 5. Inquiries (`/admin/contact/contactmessage/`)
* View all messages sent through the contact form.
* Displays sender name, email, subject, message body, submission timestamp, and client IP.
* Batch mark messages as read/unread using the admin actions dropdown.

---

## 📧 Email Notification Setup

By default, in local development (`DEBUG=True`), Django writes dispatched contact emails to the console terminal (`console.EmailBackend`).

To configure live email notifications to your inbox when someone submits the contact form, set the following environment variables in `.env`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-google-app-password
DEFAULT_FROM_EMAIL=Portfolio <noreply@yourdomain.com>
CONTACT_EMAIL=your-inbox@yourdomain.com
```

If `EMAIL_HOST` is set, the application automatically switches to Django's SMTP backend. If the email server is temporarily unreachable, the contact form catches the exception gracefully, saves the message to the database, and alerts the user without disrupting their experience.

---

## 🌐 Production Deployment

The project is structured for zero-configuration deployments on platforms such as **Render**, **Railway**, **PythonAnywhere**, or **VPS**.

### Deploying to Render
1. Push this repository to GitHub.
2. Create a new **Web Service** on Render and connect your GitHub repo.
3. Set the following environment variables on Render:
   - `PYTHON_VERSION`: `3.12.10`
   - `DEBUG`: `False`
   - `SECRET_KEY`: `<generate-a-random-50-character-key>`
   - `ALLOWED_HOSTS`: `.onrender.com,yourcustomdomain.com`
   - `CSRF_TRUSTED_ORIGINS`: `https://your-service.onrender.com,https://yourcustomdomain.com`
   - `DATABASE_URL`: *(Connect a Render PostgreSQL database URL)*
4. Set **Build Command**:
   ```bash
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py seed_data
   ```
5. Set **Start Command**:
   ```bash
   gunicorn config.wsgi:application
   ```

---

## 🔮 Future Improvements Roadmap

* [ ] Add a technical blog / engineering articles app (`blog/`) with markdown rendering and code syntax highlighting.
* [ ] Integrate GitHub API webhook to dynamically display recent commit activity.
* [ ] Add automated WebP image conversion and thumbnailing for uploaded project screenshots.
* [ ] Integrate PostgreSQL full-text search (`SearchVector`, `SearchQuery`) for case study content.

---

## 📄 License & Attribution

Designed and developed by **Joseph Ashirumah**.  
Crafted with Python &amp; Django.
