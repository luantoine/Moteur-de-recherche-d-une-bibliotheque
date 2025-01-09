FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/

COPY . /app

# dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# port 8000
EXPOSE 8000

# démarrer le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]