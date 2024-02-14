# SearchSmartly

# How to Run
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

To run this app you should have CSV, JSON and XML file in root folder

# For csv
```python manage.py import_poi_data pois.csv```

# For json
```python manage.py import_poi_data pois.json```

# For xml
```python manage.py import_poi_data pois.xml```

# View Result on Admin Panel
```python manage.py runserver```

# For Test
```python manage.py test```