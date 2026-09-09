FROM python:3.12-slim

WORKDIR /app

# Install Microsoft ODBC Driver 18 for SQL Server
RUN apt-get update && \
    apt-get install -y curl gnupg2 unixodbc && \
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY flask_api.py .
COPY customer_churn_pipeline.pkl .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "flask_api:app"]