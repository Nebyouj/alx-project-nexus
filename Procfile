web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers=1 --threads=2 --timeout=120
worker: celery -A config worker --loglevel=info --concurrency=1 --pool=solo