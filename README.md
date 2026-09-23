# Customer Churn Prediction — End-to-End ML & MLOps

An end-to-end **Customer Churn Prediction** project that combines Machine Learning, REST API development, database integration, containerization, CI/CD, and MLflow model management.

The project predicts whether a customer is likely to churn based on demographic, subscription, payment, and usage-related information.

---

## Project Overview

The project started as a Machine Learning classification application and was extended into a deployable MLOps workflow.

The final architecture includes:

* Machine Learning model development
* Data preprocessing and feature engineering
* SVC classification model
* Streamlit prediction interface
* Flask REST API
* PostgreSQL database
* Docker containerization
* Render deployment
* GitHub Actions CI
* Pytest API testing
* MLflow experiment tracking
* MLflow Model Registry
* `.skops` model artifact for production deployment

---

## Architecture

```text
                    Customer Input
                         |
                         v
                 Streamlit Application
                         |
                         v
                    Flask REST API
                         |
              +----------+----------+
              |                     |
              v                     v
        ML Prediction          PostgreSQL
              |
              v
       Customer Churn Result


        Development / MLOps Workflow

Data
  |
  v
EDA & Preprocessing
  |
  v
Model Training
  |
  v
Model Evaluation
  |
  v
MLflow Tracking
  |
  v
MLflow Model Registry
  |
  v
.skops Model Artifact
  |
  v
Docker
  |
  v
GitHub Actions CI
  |
  v
Render Deployment
```

---

## Machine Learning

### Features

The model uses the following input features:

**Numerical features**

* Age
* Monthly Charges
* Tenure Months

**Categorical features**

* Gender
* City
* Plan Type
* Payment Method

### Preprocessing

A Scikit-learn `ColumnTransformer` is used to process the input data.

Numerical features are standardized using:

```text
StandardScaler
```

Categorical features are encoded using:

```text
OneHotEncoder(handle_unknown="ignore")
```

The preprocessing and model are combined into a single Scikit-learn `Pipeline`.

### Model

The final classification model is:

```text
Support Vector Classifier (SVC)
```

The trained pipeline is stored as a `.skops` model artifact for deployment.

---

## Model Performance

The final SVC model achieved approximately:

| Metric    | Score |
| --------- | ----: |
| Accuracy  | 82.8% |
| Precision | 85.6% |
| Recall    | 92.0% |
| F1 Score  | 88.7% |

The model was evaluated on a held-out test dataset.

---

## Streamlit Application

The project includes a Streamlit application that allows users to enter customer information and receive a churn prediction interactively.

The application provides:

* Customer input form
* Real-time prediction
* Churn / non-churn result
* User-friendly prediction interface

---

## Flask REST API

The Machine Learning model is also exposed through a Flask REST API.

### Endpoint

```text
POST /predict
```

The API accepts customer information and returns:

* Customer ID
* Subscription ID
* Payment ID
* Churn prediction
* Prediction message

Example prediction:

```json
{
  "prediction": 1,
  "message": "Customer likely to churn"
}
```

Swagger/OpenAPI documentation is available through:

```text
/apidocs
```

---

## PostgreSQL Database

The Flask API stores prediction-related customer information in PostgreSQL.

The database contains tables for:

* Customers
* Subscriptions
* Payments

The API generates IDs and stores the corresponding records after a successful prediction.

---

## Docker

The Flask API is containerized using Docker.

The Docker image contains:

* Python runtime
* Application dependencies
* Flask API
* Production ML model artifact

The application runs using Gunicorn inside the container.

Example startup command:

```text
gunicorn --bind 0.0.0.0:5000 flask_api:app
```

---

## CI/CD and Testing

GitHub Actions is used to automatically test the project.

The CI workflow:

1. Checks out the repository
2. Sets up Python
3. Installs dependencies
4. Runs Pytest
5. Verifies the Flask API

The test suite currently passes successfully.

```text
2 passed
```

Important files:

```text
.github/workflows/ci.yml
pytest.ini
tests/test_api.py
```

---

## MLflow

MLflow is used for experiment tracking and model management.

The project tracks:

* Model type
* Dataset information
* Accuracy
* Precision
* Recall
* F1 score

The final SVC model was registered in the MLflow Model Registry as:

```text
CustomerChurnModel
Version 1
```

The registered model was then exported as a `.skops` artifact for production deployment.

---

## Model Deployment

The production Flask API uses:

```text
customer_churn_model.skops
```

The model is loaded using `skops.io` with the required trusted type configuration.

This allows the production API to load the trained preprocessing pipeline and SVC model without requiring the MLflow tracking server to run in production.

---

## Deployment

The Flask API is deployed as a Docker service on Render.

Production flow:

```text
GitHub
   |
   v
Render
   |
   v
Docker Build
   |
   v
Gunicorn
   |
   v
Flask API
   |
   +----> ML Model
   |
   +----> PostgreSQL
```

The deployed API was successfully tested using Swagger.

A test request successfully returned:

```text
Prediction: 1
Customer likely to churn
```

and created corresponding customer, subscription, and payment records in PostgreSQL.

---

## Project Structure

```text
Customer-Churn-Prediction/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── tests/
│   └── test_api.py
│
├── app.py
├── flask_api.py
├── create_tables.py
│
├── customer_churn.ipynb
├── customer_churn_model.skops
├── customer_churn_pipeline.pkl
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .gitignore
├── README.md
└── image_churn.jpg
```

---

## Technologies Used

### Machine Learning

* Python
* Pandas
* NumPy
* Scikit-learn
* SVC
* Joblib
* Skops

### Application Development

* Streamlit
* Flask
* Swagger / Flasgger

### Database

* PostgreSQL
* Psycopg

### MLOps

* MLflow
* MLflow Model Registry
* GitHub Actions
* Pytest
* Docker

### Deployment

* Render
* Gunicorn

---

## End-to-End Workflow

```text
Data
 ↓
EDA
 ↓
Preprocessing
 ↓
Model Training
 ↓
Model Evaluation
 ↓
MLflow Experiment Tracking
 ↓
MLflow Model Registry
 ↓
.skops Model Artifact
 ↓
Flask REST API
 ↓
Docker
 ↓
GitHub Actions CI
 ↓
Render
 ↓
PostgreSQL
```

---

## Key Learning Outcomes

This project demonstrates practical experience with:

* Building an end-to-end Machine Learning pipeline
* Handling numerical and categorical data
* Training and evaluating classification models
* Saving production-ready ML artifacts
* Building REST APIs for ML models
* Connecting APIs to PostgreSQL
* Containerizing ML applications with Docker
* Implementing automated testing with Pytest
* Setting up CI using GitHub Actions
* Tracking experiments with MLflow
* Registering models using MLflow Model Registry
* Deploying ML APIs to the cloud
* Debugging production ML compatibility issues

---

## Author

**Hari Haran**

MCA — Data Science & AI

Focus areas:

* Machine Learning
* Data Science
* AI Engineering
* MLOps
* API Development

