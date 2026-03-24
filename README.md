# Cars Dealership - Full-Stack Cloud Application

**Project Name:** Cars Dealership Web Application

**Author:** [Your Name]

**Date:** March 2026

---

## Project Overview

Cars Dealership is a responsive full-stack web application for a national car retailer in the U.S. The application displays dealership branches, allows users to view dealer details, submit reviews, and browse car makes/models. It is built with Django (backend), React/HTML (frontend), Node.js microservices, and deployed using Docker, Kubernetes, and IBM Cloud Code Engine.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, JavaScript (Vanilla), React (Register component) |
| Backend | Django 4.2, Django REST Framework |
| Microservice | Node.js, Express.js |
| Database | SQLite (Django), MongoDB-ready (Mongoose) |
| Deployment | Docker, Docker Compose, Kubernetes, IBM Cloud Code Engine |
| CI/CD | GitHub Actions |
| Auth | Django session-based authentication |

---

## Architecture

```
                    ┌─────────────────┐
                    │   Browser       │
                    │  (HTML/CSS/JS)  │
                    └────────┬────────┘
                             │ HTTP
              ┌──────────────┴──────────────┐
              │                             │
       ┌──────▼────────┐          ┌───────▼──────┐
       │ Django App    │          │ Microservice  │
       │ (Port 8000)  │          │ (Port 3000)   │
       │              │          │              │
       │ - Auth       │          │ - Dealers    │
       │ - Reviews    │          │ - MongoDB    │
       │ - CarMakes   │          └──────────────┘
       │ - Sentiment  │
       └──────┬───────┘
              │
       ┌──────▼───────┐
       │   SQLite     │
       │  (Cars DB)   │
       └──────────────┘
```

---

## Features

- **Home Page**: Lists all dealership branches with state filtering
- **About Us**: Team member profiles with contact details
- **Contact Us**: Business contact info and branch locations
- **Dealer Details**: Individual dealer info with customer reviews
- **Review System**: Users can post reviews with sentiment analysis
- **User Registration**: Sign-up with username, first name, last name, email, password
- **Admin Panel**: Django admin interface for data management
- **Car Makes/Models API**: Browse vehicle inventory

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/` | Health check |
| POST | `/api/login/` | User login |
| POST | `/api/logout/` | User logout |
| POST | `/api/register/` | User registration |
| GET | `/api/dealers/` | Get all dealers |
| GET | `/api/dealers/<state>/` | Get dealers by state |
| GET | `/api/dealers/dealer/<id>/` | Get dealer by ID |
| GET | `/api/dealers/<id>/reviews/` | Get dealer reviews |
| POST | `/api/dealers/<id>/reviews/post/` | Post a review |
| GET | `/api/carmakes/` | Get all car makes and models |
| GET | `/api/analyze/sentiment/` | Sentiment analysis |
| POST | `/api/seed/` | Seed sample data |

---

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)
- IBM Cloud CLI (for deployment)

### Local Development

#### 1. Backend (Django)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed sample data
curl -X POST http://localhost:8000/api/seed/

# Run server
python manage.py runserver
```

#### 2. Microservice (Node.js)

```bash
cd microservices
npm install
node index.js
```

#### 3. Access the Application

- **Django App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **Microservice**: http://localhost:3000

---

## Docker Deployment

```bash
# Build and run all services
docker-compose up --build

# Access the app
# Django: http://localhost:8000
# Microservice: http://localhost:3000
```

---

## Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/django-deployment.yaml
kubectl apply -f k8s/django-service.yaml
kubectl apply -f k8s/microservice-deployment.yaml
kubectl apply -f k8s/microservice-service.yaml
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -n cars-dealership
```

---

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment. The pipeline includes:

1. **Code Quality Check** (flake8 linting)
2. **Django Tests** (unit tests)
3. **Node.js Tests** (microservice tests)
4. **Docker Build & Test** (build images and run container tests)
5. **Deploy to IBM Cloud Code Engine** (on main branch push)

### Required GitHub Secrets

- `IBM_CLOUD_API_KEY`: IBM Cloud API key
- `IBM_NAMESPACE`: IBM Container Registry namespace

---

## Project Structure

```
x-final-cloud-app-with-database/
├── djangoproj/                  # Django project
│   ├── frontend/
│   │   └── static/              # Static HTML/CSS/JS
│   │       ├── index.html       # Home page
│   │       ├── About.html       # About Us page
│   │       ├── Contact.html     # Contact Us page
│   │       ├── dealer.html      # Dealer detail page
│   │       └── style.css        # Main stylesheet
│   ├── src/components/
│   │   └── Register/            # React Register component
│   ├── views.py                 # API views
│   ├── urls.py                  # URL routing
│   └── settings.py              # Django settings
├── carsapp/                     # Cars app
│   └── models.py                # CarMake, CarModel models
├── microservices/               # Node.js microservice
│   ├── index.js                 # Express server
│   └── package.json             # Node dependencies
├── k8s/                         # Kubernetes manifests
├── .github/workflows/           # GitHub Actions
├── Dockerfile                   # Django Docker image
├── Dockerfile.microservice      # Microservice Docker image
├── docker-compose.yml           # Docker Compose
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## Screenshots

Screenshots demonstrating the application functionality are saved in the root directory:

- `admin_login.png` - Admin login page
- `admin_logout.png` - Admin logout page
- `get_dealers.png` - Dealers on home page (before login)
- `get_dealers_loggedin.png` - Dealers after login
- `dealersbystate.png` - Dealers filtered by Kansas
- `dealer_id_reviews.png` - Dealer detail with reviews
- `dealership_review_submission.png` - Post review form
- `added_review.png` - Posted review
- `deployed_landingpage.png` - Deployed landing page
- `deployed_loggedin.png` - Deployed logged-in page
- `deployed_dealer_detail.png` - Deployed dealer detail
- `deployed_add_review.png` - Deployed review page

---

## License

This project was created as part of a Full-Stack Development Capstone course.
