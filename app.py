import sqlite3
import streamlit as st
import os
import google.generativeai as gai 
import openpyxl
import datetime
from db_builder import create_db
from dotenv import load_dotenv
# load environment variables
load_dotenv()

# configure gai key
# get your api key from https://makersuite.google.com/app/apikey and save it to .env file
gai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# create sql database and table
create_db()

# function using Google Gemini to convert text Question message to sql query
def gemini_response(prompt, question):
    model=gai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, question])
    return response.text

# function to retrieve query from database
def get_data(sqlQs, database):
    conn=sqlite3.connect(database)
    cur=conn.cursor()
    cur.execute(sqlQs)
    results=cur.fetchall()
    #print results
    for i in results:
        print(i)
    return results
    
# define a prompt
prompt="""
    you are an expert in converting English questions to SQL query.
    The SQL database has the name SampleSuperStore and has the following columns:
    row_ID,order_ID,order_date,ship_date,ship_mode,customer_ID,\n
    customer_name,segment,Country_Region,City,State,PostCode,\n
    Region,product_ID,category,sub_category,product_name,sales,\n
    quantity,discount,profit \n\nFor example, \nExample 1 - How many
    entries of the records are present?, the SQL command will be 
    something like this SELECT count(*) FROM SampleSuperStore; 
    \nExample 2 - Show me all the orders delivered in June 2016?,
    the SQL command will be something like this SELECT * FROM 
    SampleSuperStore WHERE ship_date between date('2016-06-01') and 
    date('2016-06-30'); you should keep all letters lowercase when 
    making function calls. additionally, the sql code should not have
    ''' in the beginning or end and sql word in output
    
    """

#Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")
# if submit is clicked
if submit:
    sqlQs=gemini_response(prompt,question)
    print(sqlQs)
    response=get_data(sqlQs,"SSS.db")
    st.subheader("The Response is")
    print(response)
    st.table( response)
    
