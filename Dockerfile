FROM python:3.13
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x prestart.sh && \
    if [ -f alembic.ini ]; then \
      ln -s /app/alembic.ini /alembic.ini; \
    fi

CMD ["/app/prestart.sh"]