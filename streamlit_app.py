import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list=my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("pick some fruits: ",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display
streamlit.dataframe(fruits_to_show)


# new section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
fruit_choice = streamlit.text_input('what fruit would you like information about ?')
# #streamlit.write('The user entered', fruit_choice)
if not fruit_choice:
  streamlit.error("please select a fruit to get information.")
  else:

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# streamlit.text(fruityvice_response.json()) # just writes the data to the screen

# take the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output it the screen as a table
streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()
  
# don't run anything past here while we troubleshoot
streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit list contains:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('what fruit would you like to add ?' , 'Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

# this will not work currently
my_cur.execute("insert into fruit_load_list values ('from steamlit')")

