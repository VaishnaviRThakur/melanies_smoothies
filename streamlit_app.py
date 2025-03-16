# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# User input for order name
name_on_order = st.text_input("Name on the Order")
st.write('The name on your Smoothie will be:', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake", type="snowflake")
session = cnx.session()

# Fetch available fruits
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()

# Extract fruit names as a list
fruit_options = [row["FRUIT_NAME"] for row in my_dataframe]

# Multiselect for choosing ingredients
ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_options, max_selections=5)

# **Fix: Properly define `ingredients_string` inside the `if` block**
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)  # Join selected fruits into a string

    # Debugging: Display selected ingredients
    st.write("Selected Ingredients:", ingredients_string)

    # SQL Insert Statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Submit button to insert data
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

