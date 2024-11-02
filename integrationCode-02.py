import pickle
import pandas as pd
import streamlit as st
from sklearn.linear_model import Lasso

# Load the final model
with open('final_model.pkl', 'rb') as file:
    final_model = pickle.load(file)

# Define model_columns based on the loaded model
# Align model columns with coefficient length and display feature importance
model_columns = (
    final_model.feature_names_in_ 
    if hasattr(final_model, 'feature_names_in_') 
    else one_hot_columns
)

# Load the one-hot encoded column names
with open('one_hot_columns.pkl', 'rb') as file:
    one_hot_columns = pickle.load(file)

# Check feature importance
feature_importance = pd.Series(final_model.coef_, index=model_columns)
st.write("Feature Importance:\n", feature_importance.sort_values(ascending=False))

# Load the dataset for selection options
df = pd.read_excel('maintenance_cleaned_extended.xlsx')

# Streamlit UI
st.title("Cost Prediction Using Lasso Regression")
service_duration_dict = {
    'اصلاح بودي':5,
    'اصلاح زجاج':1,
    'اصلاح فرش':2,
    'اصلاح كهرباء':2,
    'اصلاح كوشوك':1,
    'اصلاح مكانيك':1,
    'غيار زيت':1
    }
Kms_dict = {
    range(0,50000)      : 0.1,
    range(50000,100000) : 0.3,
    range(100000,150000): 0.5,
    range(150000,500000): 0.7,
    range(500000,999999): 0.9
    }

# Function to get the value from the dictionary based on the range
def get_kms_value(kms):
    for kms_range, value in Kms_dict.items():
        if kms in kms_range:
            return value
    return None

df['service_duration_avg_days'] = df['service_duration'].replace(service_duration_dict)
# User inputs
service_duration = st.number_input("Enter Service Duration (in days):", min_value=0)
KMs_In           = st.number_input("Enter current car kilometers:", min_value=0)
# Select boxes for categorical inputs
damage_type = st.selectbox("Select Damage Type", df['damage type'].unique())
location = st.selectbox("Select Location", df['location'].unique())

service_duration_avg_days = service_duration_dict.get(damage_type.strip())
service_probability = get_kms_value(KMs_In)

st.write('Average Service Duration in Days:', service_duration_avg_days)
st.write('Service Probability:', service_probability)

# Prediction on button click
if st.button("Predict"):
    # Create a DataFrame for the input features with `one_hot_columns`
    input_data = pd.DataFrame(columns=one_hot_columns)
    input_data.loc[0] = 0  # Initialize all values to zero

    # Fill the DataFrame with the user inputs
    input_data.at[0, 'service_duration'] = service_duration
    input_data.at[0, 'KMs_IN'] = KMs_In
    input_data.at[0, 'service_duration_avg_days'] = service_duration_avg_days
    input_data.at[0, 'service_probability'] = service_probability

    # One-hot encode categorical inputs
    location_column = f'location_{location}'
    damage_type_column = f'damage_type_{damage_type}'

    if location_column in one_hot_columns:
        input_data.at[0, location_column] = 1
    if damage_type_column in one_hot_columns:
        input_data.at[0, damage_type_column] = 1

    # Align `input_data` columns with `model_columns` for prediction
    if model_columns is not None:
        input_data = input_data.reindex(columns=model_columns, fill_value=0)

    # Make prediction
    prediction = final_model.predict(input_data)

    # Display results
    st.write(f"Predicted Cost: ${prediction[0]:.2f}")

    # Display additional insights
    st.markdown("### Insights:")
    st.write(f"- **Service Duration:** {service_duration} day")
    st.write(f"- **KMs In:** {KMs_In} km")
    st.write(f"- **Location:** {location}")
    st.write(f"- **Damage Type:** {damage_type}")
    st.write(f"- **service_duration_avg_days:** {service_duration_avg_days}")
    st.write(f"- **service_probability:** {service_probability}")

    # Optional summary interpretation
    st.write(f"This prediction suggests that given the current conditions, the service cost would be around **${prediction[0]:.2f}**.")
