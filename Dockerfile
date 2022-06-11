FROM python:3.7-slim
ENV PYTHONUNBUFFERED=TRUE
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN python3 manage.py makemigrations tagger && python3 manage.py migrate
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]