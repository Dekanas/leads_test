import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Load datasets
leads_df = pd.read_csv('leads.csv')
results_df = pd.read_csv('results.csv')

# Define login options
salespeople = ['Salesperson 1', 'Salesperson 2', 'Salesperson 3']
manager_password = 'password'

# Create login form and display leads data
login_type = st.radio("Login as:", ["Salesperson", "Manager"])
if login_type == "Salesperson":
    username = st.selectbox("Select your name:", salespeople)
    password = st.text_input("Enter your password:", type="password")
    if password == 'password':
        leads_df = leads_df[leads_df['assigned_salesperson'] == username]
        st.write(leads_df)
    else:
        st.write("Incorrect password. Please try again.")
elif login_type == "Manager":
    password = st.text_input("Enter the manager password:", type="password")
    if password == manager_password:
        # Set up grid options
        gb = GridOptionsBuilder.from_dataframe(leads_df)
        gb.configure_pagination()
        gb.configure_side_bar()
        gb.configure_selection('single')
        gridOptions = gb.build()

        # Display leads data in grid
        leads_df = AgGrid(leads_df, gridOptions=gridOptions, update_mode=GridUpdateMode.SELECTION_CHANGED)

        # Display summary data
        st.write(leads_df.groupby('assigned_salesperson')['extension_price'].agg(['sum']))
    else:
        st.write("Incorrect password. Please try again.")


# Display leads data in grid
leads_df = AgGrid(leads_df, gridOptions=gridOptions, update_mode=GridUpdateMode.SELECTION_CHANGED)


if login_type == "Manager":
    st.write(leads_df.groupby('assigned_salesperson')['extension_price'].agg(['sum']))
