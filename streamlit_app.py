# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# Input for smoothie name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get Snowflake session
#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()


# Fetch available fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Multi-select option for fruit choices
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)  # Join selected ingredients

    # SQL insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name) 
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Button to submit the order
    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()  # Execute SQL
        st.success('Your Smoothie is ordered!', icon="✅")
