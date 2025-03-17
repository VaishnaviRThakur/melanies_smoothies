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
