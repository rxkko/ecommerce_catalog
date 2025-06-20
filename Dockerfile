FROM python:3.13
COPY wait-for-it.sh .
WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .