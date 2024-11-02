import pickle
import pandas as pd
import streamlit as st
from sklearn.linear_model import Lasso

# Load the final model
with open('final_model.pkl', 'rb') as file:
    final_model = pickle.load(file)

# Load the one-hot encoded column names
with open('one_hot_columns.pkl', 'rb') as file:
    one_hot_columns = pickle.load(file)

# Streamlit UI
st.title("Cost Prediction Using Lasso Regression")

# User inputs
service_duration = st.number_input("Enter Service Duration (in hours)", min_value=0)
kms_diff = st.number_input("Enter KMs Difference", min_value=0)

# Select boxes for categorical inputs
location = st.selectbox("Select Location", ['Location1', 'Location2', 'Location3'])  # Replace with actual locations
damage_type = st.selectbox("Select Damage Type", ['Type1', 'Type2', 'Type3'])  # Replace with actual damage types
cost_category = st.selectbox("Select Cost Category", ['Category1', 'Category2', 'Category3'])  # Replace with actual categories

if st.button("Predict"):
    # Create a DataFrame for the input features
    input_data = pd.DataFrame(columns=one_hot_columns)  # Start with the full structure
    input_data.loc[0] = 0  # Initialize to zero

    # Fill the DataFrame with the user inputs
    input_data.at[0, 'service_duration'] = service_duration
    input_data.at[0, 'KMs Diff'] = kms_diff
    input_data.at[0, f'location_{location}'] = 1  # One-hot encode the selected location
    input_data.at[0, f'damage_type_{damage_type}'] = 1  # One-hot encode the selected damage type
    input_data.at[0, f'cost_category_{cost_category}'] = 1  # One-hot encode the selected cost category

    # Make prediction
    prediction = final_model.predict(input_data)
    
    # Display result
    st.write(f"Predicted Cost: ${prediction[0]:.2f}")

 # Display additional insights
    st.markdown("### Insights:")
    st.write(f"- **Service Duration:** {service_duration} hours")
    st.write(f"- **KMs Difference:** {kms_diff} km")
    st.write(f"- **Location:** {location}")
    st.write(f"- **Damage Type:** {damage_type}")
    st.write(f"- **Cost Category:** {cost_category}")

    # Optional summary interpretation
    st.write(f"This prediction suggests that given the current conditions, the service cost would be around **${prediction[0]:.2f}**.")
