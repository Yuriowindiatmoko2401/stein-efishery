# FROM ubuntu:18.04
FROM python:3.6.5-slim

# copy all file n Install dependencies:
COPY . .

RUN pip install -r requirements.txt

# Run the application:
CMD ["python", "app_etl_platform.py"]
