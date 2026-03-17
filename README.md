# Food Delivery - Internet Technology Course Project

## 🍔 Project Overview
This project is a food delivery web application that provides users with convenient online food ordering services. Main features include: user registration and login, browsing nearby restaurants and menus, managing shopping cart, filling delivery information and placing orders, real-time order tracking. It also provides merchants with menu management and order viewing functions.

## 👥 Team Members & Responsibilities

### Design Phase (based on Design Specification)
* **PEISHUO SONG (3070832S)** - Application Overview, User Stories (MoSCoW), Site Map design
* **JINQIANG KANG (3089573K)** - System Architecture Diagram, ER Diagram (compressed Chen notation)
* **SHENGZE DAI (3105381D)** - Wireframes for all key pages, Accessibility Plan (WCAG 2.2)

### Implementation Phase
* **PEISHUO SONG** - Front-end development + Git repository management
* **JINQIANG KANG** - Back-end development + Database design
* **SHENGZE DAI** - Database design + Report writing + Deployment

## 🛠️ Standard Git Workflow

**Step 1: Sync with Main**
```bash
git pull origin main
Step 2: Write Code & Commit

bash
git add .
git commit -m "feat: add shopping cart page"
Step 3: Push to GitHub

bash
git push origin main
🚀 How to Run
Create virtual environment

bash
python -m venv venv
venv\Scripts\activate  # Windows
Install dependencies

bash
pip install -r requirements.txt
Run the server

bash
python manage.py runserver
Access the app

text
http://127.0.0.1:8000/test/
📁 Project Structure
text
food_delivery/
├── accounts/          # User authentication (M1)
├── carts/             # Shopping cart (M3)
├── restaurants/       # Restaurant and menu browsing (M2)
├── orders/            # Order management (M4, M5)
├── merchants/         # Merchant management (C2)
├── reviews/           # Reviews and favorites (S1, S2, C1)
├── static/            # CSS/JS/images
│   ├── css/
│   ├── js/
│   └── img/
├── templates/         # HTML templates
│   ├── components/    # Reusable components (navbar, footer)
│   ├── accounts/
│   ├── carts/
│   ├── restaurants/
│   └── orders/
└── docs/              # Screenshots and report materials
    ├── screenshots/
    ├── accessibility/
    └── sustainability/
⚠️ Known Issues & Rules
DO NOT commit any __pycache__/, .DS_Store or db.sqlite3 files. They are already in the .gitignore.

DO NOT commit any API keys or secret keys. Use environment variables or local files.

Always test your code before pushing. Check for broken links and console errors.

Keep commit messages clear and descriptive (e.g., feat:, fix:, docs:, style:).
