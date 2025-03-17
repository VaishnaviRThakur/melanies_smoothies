# Import necessary packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Streamlit UI Header
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Text input for order name
name_on_order = st.text_input("Name on the Order")
if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# Establish Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))

# Convert to Pandas DataFrame
pd_df = my_dataframe.to_pandas()

# Multi-select dropdown for ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:", 
    pd_df["FRUIT_NAME"], 
    max_selections=5
)

# Display nutrition info if ingredients are selected
ingredients_string = ""

if ingredients_list:
    for fruit_chosen in ingredients_list:
        search_on = pd_df.loc[pd_df["FRUIT_NAME"] == fruit_chosen, "SEARCH_ON"].iloc[0]
        st.subheader(f"{fruit_chosen} Nutrition Information")

        # API call to fetch nutrition details
        try:
            response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
            if response.status_code == 200:
                st.dataframe(data=response.json(), use_container_width=True)
            else:
                st.warning(f"⚠️ Unable to fetch nutrition details for {fruit_chosen}.")
        except Exception as e:
            st.error(f"❌ API request failed: {e}")

        # Constructing the ingredient string
        ingredients_string += fruit_chosen + ", "

# Trim the last comma and space
ingredients_string = ingredients_string.strip(", ")

# Only insert if ingredients and name are provided
if ingredients_string and name_on_order:
    my_insert_stmt = "INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES (?, ?)"

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt, [ingredients_string, name_on_order]).collect()
        st.success("✅ Your Smoothie is ordered!", icon="✅")

