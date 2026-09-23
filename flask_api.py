from flask import Flask, request , jsonify
import joblib
import pandas as pd
import psycopg
import logging
import os
from dotenv import load_dotenv
from flasgger import Swagger
import traceback


load_dotenv()





app = Flask(__name__)
Swagger(app)

logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s "
)

logger = logging.getLogger(__name__)


import skops.io as sio

# Load the MLflow-generated model artifact
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "customer_churn_model.skops")

model = sio.load(
    MODEL_PATH,
    trusted=["scipy.sparse._csr.csr_matrix"]
)

def get_db_connection():

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    print("DB_HOST:", host)
    print("DB_NAME:", database)
    print("DB_USER:", username)
    print("DB_PASSWORD SET:", bool(password))

    connection = psycopg.connect(
        host=host,
        port=port,
        dbname=database,
        user=username,
        password=password,
        sslmode="require"
    )

    return connection

@app.route("/env_check", methods=["GET"])
def env_check():

    return jsonify({
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT"),
        "DB_NAME": os.getenv("DB_NAME"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASSWORD_SET": bool(os.getenv("DB_PASSWORD"))
    })

@app.route("/test_db", methods=["GET"])
def test_db():
    """
    Test PostgreSQL  connection
    ---
    responses:
      200:
        description: PostgreSQL connection successful
    """

    connection = get_db_connection()

    connection.close()

    return "PostgreSQL connection successful", 200

@app.route("/", methods=["GET"])
def home_page():
    return "Customer Churn API is running successfully"

@app.route("/customer_churn", methods = ["GET","POST"])

def home():
    return "Customer churn Flask  API  is running"

@app.route("/predict", methods = ["POST"])
def predict():
    """
    Predict customer churn
    ---
    tags:
      - Customer Churn
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: header
        name: x-api-key
        type: string
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - customer_name
            - age
            - gender
            - city
            - plan_type
            - monthly_charges
            - tenure_months
            - payment_method
          properties:
            customer_name:
              type: string
              example: Rahul
            age:
              type: integer
              example: 35
            gender:
              type: string
              example: Male
            city:
              type: string
              example: Bangalore
            plan_type:
              type: string
              example: Premium
            monthly_charges:
              type: number
              example: 75.5
            tenure_months:
              type: integer
              example: 12
            payment_method:
              type: string
              example: UPI
    responses:
      200:
        description: Prediction completed successfully
      400:
        description: Invalid input
      401:
        description: Unauthorized
      500:
        description: Server error
    """
     
    api_key = request.headers.get("x-api-key")

    print("Received API key:", api_key)
    print("Expected API key:", os.getenv("API_KEY"))

    if api_key != os.getenv("API_KEY"):
        return jsonify({
            "status": "error",
            "message": "Unauthorized"
        }), 401

    connection = None
    cursor = None


    try:
        #logger info
        logger.info("Prediction  request received")

        #get json data from postman   
        data = request.json

        required_fields = [
        "customer_name",
        "age",
        "gender",
        "city",
        "plan_type",
        "monthly_charges",
        "tenure_months",
        "payment_method"]

        missing_fields = [
        field for field in required_fields
        if field not in data
        ]

        if missing_fields:
             return jsonify({
                "status": "error",
                "message":"Required fileds are missing",
                "error": missing_fields
            }), 400

        try:
            age = int(data["age"])

        except (ValueError, TypeError):
            return jsonify({
                "status":"error",
                "error": "age must be an integer"
            }), 400

        try:
            monthly_charges = float(data["monthly_charges"])
        except (ValueError, TypeError):
            return jsonify({
                "status":"error",
                "error": "monthly_charges must be a number"
            }), 400

        try:
            tenure_months = int(data["tenure_months"])
        except (ValueError, TypeError):
            return jsonify({
                "status":"error",
                "error": "tenure_months must be an integer"
            }), 400

        if age <= 0:
            return jsonify({
                "status": "error",
                "message": "Invalid age",
                "error": "Age must be greater than 0"
            }), 400

        if monthly_charges <= 0:
            return jsonify({
                "status": "error",
                "message": "Invalid montly charges",
                "error": "Monthly charges must be greater than 0"
            }), 400

        if tenure_months < 0:
            return jsonify({
                "status": "error",
                "message": "Invalid tenure month",
                "error": "Tenure months cannot be negative"
            }), 400
        
        if data["gender"] not in ["Male", "Female","male","female"]:
            return jsonify({
                "error": "gender must be Male or Female"
                }), 400
        if data["plan_type"] not in [
            "Basic",
            "Standard",
            "Premium"
        ]:
            return jsonify({
                "error": "plan_type must be Basic, Standard or Premium"
            }), 400
        if data["payment_method"] not in [
            "UPI",
            "Credit Card",
            "Debit Card"
        ]:
            return jsonify({
                "error": "payment_method must be UPI, Credit Card or Debit Card"
            }), 400

        #create dataframe
        df = pd.DataFrame([data])

        #make prediction
        prediction = model.predict(df)[0]
        logger.info("ML prediction completed")

        if prediction  ==1:
            message = "Customer likely to churn"
        else:
            message = "Customer unlikey to churn"

        #connect to sql
        connection = get_db_connection()
        logger.info("Database connection established")

        cursor  = connection.cursor()

        # Generate next customer id
        cursor.execute("""
            SELECT COALESCE(MAX(customer_id), 0) + 1
            FROM customers
        """)
        customer_id = cursor.fetchone()[0]

        # Generate next subscription id
        cursor.execute("""
            SELECT COALESCE(MAX(subcription_id), 0) + 1
            FROM subscriptions
        """)
        subcription_id = cursor.fetchone()[0]

        # Generate next payment id
        cursor.execute("""
            SELECT COALESCE(MAX(payment_id), 0) + 1
            FROM payments
        """)
        payment_id = cursor.fetchone()[0]

        #insert customer
        # Insert customer
        cursor.execute("""
            INSERT INTO customers
            (customer_id, customer_name, age, gender, city, churn)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            customer_id,
            data['customer_name'],
            data['age'],
            data['gender'],
            data['city'],
            int(prediction)
        ))

        #insert subscription
        # Insert subscription
        cursor.execute("""
            INSERT INTO subscriptions
            (subcription_id, customer_id, plan_type, monthly_charges, tenure_months)
            VALUES (%s, %s, %s, %s, %s)
        """,
        (
            subcription_id,
            customer_id,
            data['plan_type'],
            data['monthly_charges'],
            data['tenure_months']
        ))

        #insert payment 
        # Insert payment
        cursor.execute("""
            INSERT INTO payments
            (payment_id, customer_id, payment_method)
            VALUES (%s, %s, %s)
        """,
        (
            payment_id,
            customer_id,
            data['payment_method']
        ))

        #save all changes
        connection.commit()
        logger.info("Customer data saved successfully")

        #close database connection
        #cursor.close()
        #connection.close()

        #return jsonify
        return jsonify({
            "status":"success",
            "message":"Prediction Completed Successfully",
            "data":{
                "customer_id":customer_id,
                "subscription_id":subcription_id,
                "payment_id":payment_id,
                "prediction": int(prediction),
                "message":message
            }
        }),201
    
    except Exception as e:
        logger.exception("Prediction API failed")
        
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "error": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc()
        }), 500

    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
