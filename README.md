

# Mini-Digi 🛒

**An AI-powered e-commerce platform built with Django, featuring intelligent product recommendations and a conversational shopping assistant named "Vex".**

---

## 🚀 Overview

Mini-Digi is a full-featured, production-grade e-commerce web application that combines a modern, responsive frontend with a robust Django backend. It integrates an intelligent chatbot assistant, "Vex," to provide users with personalized product recommendations, real-time support, and a seamless shopping experience.

### 🌟 Key Features

- **Product Catalog:** Browse, search, and filter products by category, price, and other attributes.
- **Intelligent Chatbot (Vex):** An AI-powered assistant that helps users find products, answers queries, and provides recommendations.
- **Dynamic Shopping Cart:** Add, update, and remove items with real-time price calculations.
- **Order Management:** Secure checkout process, order placement, and user order history.
- **User Authentication:** Secure sign-up, login, and profile management powered by Django-Allauth.
- **Responsive & Modern UI:** A polished, mobile-first frontend built with Tailwind CSS and custom styles.
- **Admin Dashboard:** Comprehensive admin panel for managing products, categories, orders, and users.

---

## 🏗️ Project Architecture

### 📁 Project Structure

```
mini-digi/
├── .env                    # Environment variables
├── .gitignore
├── .dockerignore
├── Dockerfile              # Docker container configuration
├── docker-compose.yml
├── flowchart.txt           # Full project file tree
├── HOW_TO_INTEGRATE.md
├── LICENSE
├── manage.py
├── README.md
├── requirements.txt        # Python dependencies
├── robots.txt
├── .github/                # CI/CD configuration
│   ├── workflow-notifications.yml
│   └── workflows/
│       ├── docker-build.yml
│       ├── notification-sender.yml
│       └── test.yml
├── management/             # Project-level management commands
│   └── commands/
│       └── compile_with_date.py
├── mini_digi/              # Project settings and configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── middleware.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── wsgi.py
│   └── views/
│       └── products.py
├── migrations/             # Project-level migrations
│   └── 0001_initial.py
├── shop/                   # Core product and catalog application
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── tests.py
│   ├── urls.py
│   ├── validators.py
│   ├── management/
│   │   └── commands/
│   │       ├── 0004_product_available.py
│   │       └── seed_products.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cart_models.py
│   │   ├── category.py
│   │   ├── newsletter.py
│   │   ├── product.py
│   │   └── product_image.py
│   ├── templatetags/
│   │   ├── emoji_tags.py
│   │   └── shop_tags.py
│   ├── views/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── contact.py
│   │   ├── newsletter.py
│   │   └── products.py
│   └── migrations/         # 12 migrations (0001-0009, 0011-0012)
├── cart/                   # Shopping cart application
│   ├── context_processors.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── orders/                 # Order management application
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── dashboard/              # User dashboard application
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── support/                # Support & ticketing application
│   ├── admin.py
│   ├── context_processors.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   └── templatetags/
│       └── support_tags.py
├── locale/                 # Internationalization (de, es, fr, ru)
├── static/                 # Static assets (CSS, JavaScript, images, fonts)
│   ├── css/
│   ├── js/
│   ├── lib/
│   ├── img/
│   └── fonts/
├── media/                  # User-uploaded media
│   ├── categories/
│   ├── products/
│   └── tickets/
│       └── attachments/
└── templates/              # Django HTML templates
    ├── base.html
    ├── account/            # Allauth authentication templates
    ├── cart/
    ├── components/         # Reusable partials (navbar, footer, card)
    ├── dashboard/          # User dashboard (profile, orders, tickets, wishlist)
    ├── orders/             # Checkout & confirmation
    ├── partials/
    ├── shop/
    └── support/
```

---

## 💻 Technology Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Django** | Web framework (Python 3.10) |
| **Django-Allauth** | Authentication & user management |
| **Django Crispy Forms** | Form rendering & styling |
| **SQLite** | Development database |
| **Pillow** | Image processing & manipulation |
| **Django Tailwind** | UI framework integration |

### Frontend
| Technology | Purpose |
|------------|---------|
| **Tailwind CSS** | Utility-first CSS framework |
| **Bootstrap 5** | Responsive layout & components |
| **Owl Carousel** | Product carousels & sliders |
| **Font Awesome** | Icons & UI elements |
| **Animate.css** | CSS animations |
| **JavaScript (Vanilla)** | Dynamic UI interactions |

### AI & Integrations
| Technology | Purpose |
|------------|---------|
| **Vex (AI Assistant)** | Intelligent product recommendations & chat support |
| **n8n** | Workflow automation for backend tasks |
| **Docker** | Containerization & deployment |
| **Git/GitHub** | Version control & collaboration |

### Deployment
| Technology | Purpose |
|------------|---------|
| **GitHub Actions** | CI/CD pipeline |
| **Docker Hub** | Container registry |
| **Netlify** | Frontend hosting |
| **Heroku/AWS** | Backend deployment |

---

## 🤖 AI Assistant: Vex

"Vex" is an intelligent chatbot integrated into the Mini-Digi platform to enhance the user experience. It provides:

- **Product Discovery:** Users can ask for product recommendations based on their preferences.
- **Instant Support:** Answers frequently asked questions about products, shipping, and returns.
- **Personalized Suggestions:** Analyzes user behavior and browsing history to offer tailored product recommendations.
- **Conversational Interface:** A natural language interface that feels like chatting with a human assistant.

**Vex is designed to make shopping intuitive, engaging, and efficient.**

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/cmd-3324/mini-digi.git
cd mini-digi
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root with the following variables:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Seed the Database with Sample Products
```bash
python manage.py seed_products
```

### 8. Run the Development Server
```bash
python manage.py runserver
```

Your application will be accessible at **http://127.0.0.1:8000**

---

## 🐳 Docker Deployment

### Build the Docker Image
```bash
docker build -t mini-digi .
```

### Run the Container
```bash
docker run -p 8000:8000 mini-digi
```

---

## 📜 Development Scripts

| Command | Description |
|---------|-------------|
| `python manage.py seed_products` | Populate database with sample product data |
| `python manage.py tailwind start` | Start Tailwind CSS build process |
| `python manage.py collectstatic` | Collect static files for production |
| `python manage.py test` | Run test suite |
| `docker-compose up` | Start application with Docker Compose |

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Homepage with featured products |
| `/products/` | GET | Product listing with filters & search |
| `/products/<id>/` | GET | Product detail page |
| `/cart/` | GET/POST | View and manage shopping cart |
| `/orders/checkout/` | GET/POST | Checkout and place orders |
| `/accounts/` | GET/POST | User authentication (login/signup) |
| `/chatbot/` | POST | AI assistant (Vex) interaction endpoint |

---

## 🎯 Key Design Decisions

1. **Modular Architecture:** Each application (`shop`, `cart`, `orders`, `support`) is self-contained and loosely coupled.
2. **Split Views & Models:** Improves maintainability and organization of complex components.
3. **AI Integration:** Vex is designed to be extensible, allowing for future integration with advanced NLP models.
4. **Responsive by Default:** The frontend is built with a mobile-first approach to ensure a seamless experience across all devices.
5. **Developer Experience:** Comprehensive documentation, seed data, and Docker support reduce onboarding time.

---

## 🤝 Contributing

Contributions to Mini-Digi are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

---

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## 📬 Contact & Community

- **Author:** Max (cmd-3324)
- **Email:** programmers378@gmail.com
- **Whatsapp:** @minidigiSupport
- **GitHub:** [cmd-3324](https://github.com/cmd-3324)
- **Project Link:** [https://github.com/cmd-3324/mini-digi](https://github.com/cmd-3324/mini-digi)

---

**© 2026 Mini-Digi. All rights reserved.**
