# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("🥤Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('search_on'))

for fruit_chosen in ingredients_list:
    # Get the actual search term from the Snowflake table
    search_value = my_dataframe.filter(col('FRUIT_NAME') == fruit_chosen).to_pandas().iloc[0]['SEARCH_ON']

    # Show the subheader
    st.subheader(fruit_chosen + ' Nutrition Information')

    # API call
    smoothie_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_value}")

    # Display the result
    st.dataframe(data=smoothie_response.json(), use_container_width=True)

#st.dataframe(data=my_dataframe, use_container_width=True)

import requests
#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
#sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

# Text input for the custom smoothie name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)



ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe )

#.to_pandas()["FRUIT_NAME"].tolist(), max_selection = 5

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


  #st.write(ingredients_string)


  #my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            #values ('""" + ingredients_string + """')"""
    
  my_insert_stmt = (
        """INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('""" + ingredients_string.strip() + """', '""" + name_on_order + """')"""
    )


  #st.write(my_insert_stmt)
  #st.stop()

  time_to_insert = st.button('Submit Order')

  if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
