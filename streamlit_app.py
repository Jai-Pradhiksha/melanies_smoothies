import streamlit as st 
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:") 
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for name on the order
name_on_order = st.text_input("Name on Smoothie:")
st.write(f'The name on your Smoothie will be: {name_on_order}')

# Get active session
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit options from the Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(my_dataframe, use_container_width=True)

# Multiselect for choosing ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', 
    my_dataframe,  # Collecting rows to list for Streamlit multiselect
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # Insert statement preparation
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order) 
    VALUES ('{ingredients_string}', '{name_on_order}')
    """

    st.write(my_insert_stmt)

    # Submit button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered! {name_on_order}', icon="✅")
