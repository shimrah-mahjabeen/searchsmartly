# SearchSmartly

# Navigate to the project directory
cd searchsmartly

# Set up a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser for the Django Admin Panel
python manage.py createsuperuser

# Runserver
python manage.py runserver