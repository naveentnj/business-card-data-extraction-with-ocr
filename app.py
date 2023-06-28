import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import easyocr
import streamlit as st
st. set_page_config(layout="wide")
import re
import sql_module
import processing_module
from processing_module import format_title
import numpy as np
from PIL import Image

# Use the function to format your title
st.markdown(format_title("BUSINESS CARDS DATA EXTRACTION AND MANAGEMENT WITH OCR AND SQL"), unsafe_allow_html=True)

st.write("\n \n \n ")
#st.write(" ")
#st.write(" ")
st.write("### UPLOAD ANY BUSINESS CARD IMAGE TO EXTRACT INFORMATION ")
CD,col1, col2,col3= st.columns([0.5,4,1,4])
with col1:
    #image uploader
    st.write("#### SELECT IMAGE")
    image = st.file_uploader(label = "",type=['png','jpg','jpeg'])

@st.cache_data
def load_model(): 
    reader = easyocr.Reader(['en'], gpu = True)
    return reader 

reader = load_model()

if image is not None:
    input_image = Image.open(image) #read image
    with col1:
        st.write("## Input Image")
        st.image(input_image) #display image        
    
    result = reader.readtext(np.array(input_image))
    result_text = [] 
    for text in result:
        result_text.append(text[1])

    #st.write(result_text)

    regex_result = processing_module.regex(result_text)
    phoneNumber= []
    phoneID=[]  
    address=set()
    addressID=[]
    emailAddress = regex_result[0]
    emailID= regex_result[0]
    st.write(emailID)
    Pincode=''
    PinID=''
    website=''
    webID=''

with col3: 
    # DISPLAY ALL THE ELEMENTS OF BUSINESS CARD 
    st.write("## EXTRACTED TEXT")
    st.write('##### :red[WEBSITE URL: ] '+ str(WEB))
    st.write('##### :red[EMAIL: ] '+ str(EMAIL)) 
    st.write('##### :red[PIN CODE: ] '+ str(PIN)) 
    ph_str = ', '.join(PH)
    st.write('##### :red[PHONE NUMBER(S): ] '+ph_str)
    add_str = ' '.join([str(elem) for elem in ADD])
    st.write('##### :red[ADDRESS: ] ', add_str)

    IDS= [EID,PID,WID]
    IDS.extend(AID)
    IDS.extend(PHID)

choice = ""

menu = ['Upload', 'View', 'Update', 'Delete']

upload = st.button("Upload extracted data and interact with db")

if upload:
  choice = st.sidebar.selectbox("Select an option", menu)

val = [('Peter', 'Lowstreet 4'),
  ('Amy', 'Apple st 652'),
  ('Hannah', 'Mountain 21'),
  ('Michael', 'Valley 345'),
  ('Sandy', 'Ocean blvd 2'),
  ('Betty', 'Green Grass 1') ]

if choice == menu[0]:
    st.write(sql_module.add(val))
elif choice == menu[1]:
    rows = 10
    st.dataframe(sql_module.view(rows))
else:
    st.write("## Thank you")


