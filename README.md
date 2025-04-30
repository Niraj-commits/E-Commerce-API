#EasyBuy-API – E-commerce Backend with Django REST Framework

EasyBuy-API is a RESTful backend for an e-commerce platform built using Django and Django REST Framework (DRF). It supports user roles like customers, sellers, delivery personnel, and admins. The API manages products, orders, user registration, and delivery tracking.

##Tools & Technologies
- **Backend**: Django, Django REST Framework,drf-spectacular
- **Database**: SQLite (development)
- **Authentication**: Token-based auth
- **Version Control**: Git, GitHub

##Features
- User roles: Admin, Supplier, Customer, Delivery Personnel
- Product creation and listing (supplier only)
- Order creation and order tracking
- Delivery management and status updates
- Email push notifications on delivery status
- Dynamic total cost calculation in serializers
- Secure registration and login system

##How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/Niraj-commits/EasyBuy-API.git
   cd EasyBuy-API
2. Create annd activate a virtual environment
   ```bash
   python -m venv env
   source env/bin/activate   # For Linux/Mac
   env\Scripts\activate      # For Windows
3. Install Dependencies
   ```bash
   pip install -r requirement.txt
4. Apply Migrations
   ```bash
   python manage.py makemigrations
   python manage.py migrate
5. Create Superuser and Run the server
   ```bash
   python manage.py createsuperuser
   python manage.py runserver
