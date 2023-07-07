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
import io

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
    #st.write(regex_result)

    emailAddress = regex_result[0]
    emailID= regex_result[1]
    Pincode = regex_result[2]
    PinID = regex_result[3]
    phoneNumberList = regex_result[4]
    phoneID=regex_result[5]  
    address = regex_result[6]
    addressID = regex_result[7]
    website = regex_result[8]
    webID= regex_result[9]

    with col3: 
            # DISPLAY ALL THE ELEMENTS OF BUSINESS CARD 
            st.write("#### EXTRACTED TEXT")
            st.write('##### :blue[WEBSITE URL: ] '+ str(website))
            st.write('##### :blue[EMAIL: ] '+ str(emailAddress)) 
            st.write('##### :blue[PIN CODE: ] '+ str(Pincode)) 
            ph_str = ', '.join(phoneNumberList)
            st.write('##### :blue[PHONE NUMBER(S): ] '+ph_str)
            add_str = ' '.join([str(elem) for elem in address])
            st.write('##### :blue[ADDRESS: ] ', add_str)
            IDS= [emailID,PinID,phoneID,addressID,webID]
            oth=''                               
            fin=[]                        
            for i, string in enumerate(result_text):
                if i not in IDS:
                    if type(string) != int and len(string) >= 4 and ',' not in string and '.' not in string and 'www.' not in string:
                        if not re.match("^[0-9]{0,3}$", string) and not re.match("^[^a-zA-Z0-9]+$", string):
                            numbers = re.findall('\d+', string)
                            if len(numbers) == 0 or all(len(num) < 3 for num in numbers) and not any(num in string for num in ['0','1','2','3','4','5','6','7','8','9']*3):
                                fin.append(string)
            st.write('##### :blue[CARD HOLDER & COMPANY DETAILS: ] ')
            for i in fin:
                st.write('##### '+i)
                
            UP= st.button('UPLOAD TO DATABASE')

# DATABASE CODE
    websiteUpload = str(website)
    email=str(emailAddress)
    pincode=str(Pincode)
    phoneno=ph_str
    address=add_str
    det_str = ' '.join([str(elem) for elem in fin])
    details=det_str
    image.seek(0)
    image_data = image.read()

# IF UPLOAD BUTTON IS ON, THE DATA IS UPLOADED TO DATABASE
    if UP:
        if image is not None:
            # Read image data
            # Insert image data into MySQL database
            data = (website, email, pincode , phoneno, address, details, image_data)
            sql_module.add(data)
        else:
            st.write('Please upload business card')
st.write(' ')
st.write(' ')

col1.markdown("<style>div[data-testid='stHorizontalBlock'] { background-color: rgb(230, 0, 172, 0.1); }</style>", unsafe_allow_html=True)
# DATABASE PART
st.write('### EXPLORE BUSINESS CARDS DATABASE ')
cd, c1, c2,c3= st.columns([0.5, 4,1,4])
with c1: 
    st.write(' ')
    st.write("#### BUSINESS CARDS AVAILABLE IN DATABASE")
    rows = sql_module.getRowsID()
    l=[]
    # DISPLAY ALL THE CARDS AS BUTTONS
    for row in rows:
        l.append(row[0])
        button_label = f"SHOW BUSINESS CARD: {row[0]}"
        if st.button(button_label):
            row1 = sql_module.fetchRow(row[0])
            website_url = row1[1]
            email = row1[2]
            pin_code = row1[3]
            phone_numbers = row1[4]
            address = row1[5]
            card_holder_details = row1[6]

            # DISPLAY SELECTED CARD DETAILS
            with c3:                     
                st.write(f"#### BUSINESS CARD {row[0]} DETAILS ")                
                st.write(f"Website: {website_url}")
                st.write(f"Email: {email}")
                st.write(f"PIN Code: {pin_code}")
                st.write(f"Phone Numbers: {phone_numbers}")
                st.write(f"Address: {address}")
                st.write(f"Card Holder & Company Details: {card_holder_details}")

                # If the button is clicked, display the corresponding row
                rowImage = sql_module.fetchRecordImage(row[0])
                if rowImage is not None:
                    image_data = rowImage[0]
                    image = Image.open(io.BytesIO(image_data))
                    st.image(image)
                st.write(' ')  

# DELETE MULTIPLE ENTRIES                   
with c1:
    st.write(' ')
    st.write(f"#### SELECT ENTRIES TO DELETE") 
    selected_options = st.multiselect('', l)

    if st.button('DELETE SELECTED ENTRIES'):
        for option in selected_options:
            cursor.execute("DELETE FROM business_card_data WHERE id = " +str(option))
        mydb.commit()
        st.write("DELETED SELECTED BUSINESS CARD ENTRIES SUCCESSFULLY")
    st.write(' ')                
                
    





