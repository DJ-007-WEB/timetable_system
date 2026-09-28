FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt
COPY backend /app/backend
COPY frontend /app/frontend
WORKDIR /app/backend
ENV PYTHONUNBUFFERED=1
EXPOSE 5000
CMD ["gunicorn","--workers","2","--threads","4","--timeout","120","--bind","0.0.0.0:5000","app:app"]
