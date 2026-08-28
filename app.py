import streamlit as st
import pandas as pd
import joblib
import base64


#defing image
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


img = get_base64_image("image_churn.jpg")

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(f"""
<style>

.stApp {{
    background-image:
        linear-gradient(
            rgba(15, 32, 39, 0.82),
            rgba(15, 32, 39, 0.82)
        ),
        url("data:image/jpeg;base64,{img}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* Main container */
.block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
}}

/* Title */
.main-title {{
    text-align: center;
    color: white;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}}

/* Subtitle */
.subtitle {{
    text-align: center;
    color: #d6e4ea;
    font-size: 18px;
    margin-bottom: 35px;
}}

/* Section title */
.section-title {{
    color: white;
    font-size: 24px;
    font-weight: 600;
    margin-top: 10px;
    margin-bottom: 15px;
}}

/* Input labels */
label {{
    color: white !important;
    font-weight: 600 !important;
}}

/* Text input */
.stTextInput input,
.stNumberInput input {{
    border-radius: 8px;
}}

/* Select boxes */s
.stSelectbox > div > div {{
    border-radius: 8px;
}}

/* Predict button */
.stButton > button {{
    width: 100%;
    height: 55px;
    background: #00c853;
    color: white;
    font-size: 20px;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    margin-top: 20px;
}}

.stButton > button:hover {{
    background: #00a844;
    color: white;
}}

/* Result card */
.result-card {{
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    margin-top: 25px;
}}

/* Result text */
.result-title {{
    color: white;
    font-size: 28px;
    font-weight: 700;
}}

.result-description {{
    color: #d6e4ea;
    font-size: 17px;
}}

/* Footer */
.footer {{
    text-align: center;
    color: #b8cbd2;
    font-size: 14px;
    margin-top: 40px;
}}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Load Model
# --------------------------------------------------

model = joblib.load("customer_churn_pipeline.pkl")


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="main-title">📊 Customer Churn Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Predict whether a customer is likely to churn based on their profile and subscription details.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# Customer Information
# --------------------------------------------------

st.markdown(
    '<div class="section-title">👤 Customer Information</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=35
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

with col2:

    city = st.text_input(
        "City",
        placeholder="Enter city name"
    )

    payment_method = st.selectbox(
        "Payment Method",
        ["UPI", "Credit Card", "Debit Card"]
    )


# --------------------------------------------------
# Subscription Information
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📋 Subscription Details</div>',
    unsafe_allow_html=True
)

col3, col4, col5 = st.columns(3)

with col3:

    plan_type = st.selectbox(
        "Plan Type",
        ["Basic", "Standard", "Premium"]
    )

with col4:

    monthly_charges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        value=499.0,
        step=1.0
    )

with col5:

    tenure_months = st.number_input(
        "Tenure (Months)",
        min_value=0,
        max_value=120,
        value=12
    )


# --------------------------------------------------
# Prediction
# --------------------------------------------------

if st.button("🔮 Predict Churn"):

    if city.strip() == "":
        st.warning("⚠️ Please enter the City name.")

    else:

        new_customer = pd.DataFrame(
            {
                "age": [age],
                "monthly_charges": [monthly_charges],
                "tenure_months": [tenure_months],
                "gender": [gender],
                "city": [city],
                "plan_type": [plan_type],
                "payment_method": [payment_method]
            }
        )

        # Prediction
        prediction = model.predict(new_customer)

        # --------------------------------------------------
        # Display Result
        # --------------------------------------------------

        if prediction[0] == 1:

            st.markdown(
                """
                <div class="result-card">
                    <div class="result-title">
                        ⚠️ Customer is Likely to Churn
                    </div>
                    <div class="result-description">
                        This customer has been classified as likely to leave the service.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="result-card">
                    <div class="result-title">
                        ✅ Customer is Not Likely to Churn
                    </div>
                    <div class="result-description">
                        This customer has been classified as likely to remain with the service.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        Customer Churn Prediction | Machine Learning Project | By- Hari
                </div>
    """,
    unsafe_allow_html=True
)