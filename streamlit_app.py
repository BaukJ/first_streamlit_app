import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')


streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt").set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")

def get_fruit_data(fruit):
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit}")
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        fruit_data = get_fruit_data(fruit_choice)
        streamlit.dataframe(fruit_data)
except URLError as e:
    streamlit.error()



def insert_fruit(fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute(f"insert into fruit_load_list values ('{fruit}')")
        return f"Thanks for adding {fruit}"

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("Available fruits:")
streamlit.dataframe(my_data_rows)


add_fruit = streamlit.text_input('What fruit would you like to add to DB?')
if streamlit.button('Add a fruit to the List'):
    streamlit.text(insert_fruit(add_fruit))
