import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, AgGridColumn

# Load datasets
leads_df = pd.read_excel('Leads_test.xlsx')
results_df = pd.read_excel('results_test.xlsx')

# Define login options
salespeople = ['Miglė', 'Paulius', 'Justina']
manager_password = 'password'


# Define status options
status_options = ['', 'Contacted', 'Not interested', 'Follow up']


# Create login form and display leads data
login_type = st.radio("Login as:", ["Salesperson", "Manager"])
if login_type == "Salesperson":
    username = st.selectbox("Select your name:", salespeople)
    password = st.text_input("Enter your password:", type="password")
    if password == 'password':
        leads_df = leads_df[leads_df['salesmen'] == username]
        # Add new column for lead status
        leads_df['status'] = [''] * len(leads_df)
        # Define column definitions for status column
        status_column = {
            'field': 'status',
            'editable': True,
            'cellEditor': 'agSelectCellEditor',
            'cellEditorParams': {
                'values': status_options
            }
        }

        # Display leads data with status column
        leads_df = AgGrid(leads_df[['id_contract', 'product_group', 'phone', 'salesmen']], 
                          column_defs=[status_column],
                          gridOptions={'editable': True, 'enableRangeSelection': True, 'enableCellChangeFlash': True},
                          update_mode=GridUpdateMode.VALUE_CHANGED)
    else:
        st.write("Incorrect password. Please try again.")
elif login_type == "Manager":
    password = st.text_input("Enter the manager password:", type="password")
    if password == manager_password:
        # Add new column for lead status
        leads_df['status'] = [''] * len(leads_df)

        # Define column definitions for status column
        status_column = {
            'field': 'status',
            'cellEditor': 'agSelectCellEditor',
            'cellEditorParams': {
                'values': status_options
            }
        }

        # Set up grid options
        gb = GridOptionsBuilder.from_dataframe(leads_df)
        gb.configure_pagination()
        gb.configure_side_bar()
        gb.configure_selection('single')
        gb.configure_grid_options(domLayout='autoHeight')
        gb.configure_column('status', editable=True, cellEditor='agSelectCellEditor', cellEditorParams={
            'values': status_options
        })
        gridOptions = gb.build()

        # Display leads data in grid
        leads_df = AgGrid(leads_df, column_defs=[status_column], gridOptions=gridOptions, update_mode=GridUpdateMode.SELECTION_CHANGED)

        # Display summary data
        st.write(leads_df.groupby('salesmen')['phone'].agg(['count']))
    else:
        st.write("Incorrect password. Please try again.")
