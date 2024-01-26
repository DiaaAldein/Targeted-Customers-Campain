
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sklearn

# Loading the dataset
data = pd.read_csv('segmented_data.csv')

# Loading the user list
user_list = joblib.load('user_list.pkl')

# Creating a function that takes user ID and provides the best merchants for each category of customer interest
def user_best_merch(user_id):
    # Retrieve the RFM segment value for the user
    rfm_segment_value = data[data['user_id'] == user_id]['rfm_segment'].iloc[0]
    
    # Group data by the RFM segment value
    group_segment = data[data['rfm_segment'] == rfm_segment_value]
    
    # Get the total points in the user's account wallet
    total_points = data[data['user_id'] == user_id]['points'].sum()
    
    # Prepare the message
    message = f"Dear Valued Customer {user_id},\n\n"
    message += f"We'd like to remind you that you currently have ({total_points}) points in your account wallet, \nequivalent to ({total_points * 0.1})."
    message += " You can use these points to shop from our carefully selected \nlist of premier merchants across various categories:\n\n"
    
    # Iterate over unique categories in the user's group_segment
    for category in group_segment['category'].unique():
        # Get data for each specific category in the user's group_segment
        cat_data = group_segment[group_segment['category'] == category]
        
        message += f'Category: **{category}**\n'
        # Add the list of best 3 merchants per user category to the message
        message += f"{cat_data['mer_name'].value_counts().nlargest(3).index.tolist()}\n\n"
     
    message += 'Thank you for being a valued member of our community!\n\n'
    message += 'Best Regards,\n'
    
    return message


def main():
    st.title('User Targeted Offers')
    
    user_id = st.selectbox('Select user_id', user_list)
    
    if st.button(f"Target Offers for user with user id = {user_id}"):
        result = user_best_merch(user_id)
        st.write("User Target Offer")
        st.text(result)  # Display the message returned by the function

main()
