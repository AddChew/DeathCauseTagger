FROM python:3
ENV PYTHONUNBUFFERED=TRUE
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt