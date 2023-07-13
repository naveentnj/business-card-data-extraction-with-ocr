import Levenshtein
import re
import streamlit as st

def format_title(title: str):
    """
    Formats the given title with a colored box and padding
    """
    formatted_title = f"<div style='padding:10px;background-color:rgb(0, 77, 229);border-radius:10px'><h1 style='color:rgb(255, 255, 255);text-align:center;'>{title}</h1></div>"
    return formatted_title

def removeSpace(string):
    return string.replace(" ", "")


def checkRegex(inputArray):
    phoneNumber= []
    phoneID=[]  
    address=set()
    addressID=[]
    emailAddress = ""
    emailID= 0
    #st.write(emailID)
    Pincode=''
    PincodeID=''
    website=''
    webID=''
    for i, string in enumerate(inputArray):  
        #st.write(string)
                    
        # TO FIND EMAIL
        email_regex = r'([a-zA-Z0-9\.-]+)@([a-zA-Z\.-]+)([a-z]{2,6})'
        if re.search(email_regex, string.lower()):
            emailAddress = string.lower()
            emailID = i
            #st.write("email_found")
        
        # TO FIND PINCODE
        pincode_regex = r'([0-9]{3})(\s*)?([0-9]{3})'
        match = re.search(pincode_regex, string.lower())
        if match:
            Pincode=match.group()
            PincodeID=i

        phoneRegex = re.search(r'(?:ph|phone|phno)?\s*(?:[+-]?\d\s*[\(\)]*){7,}', string)
        if phoneRegex and len(re.findall(r'\d', string)) > 8:
            phoneNumber.append(string)
            phoneID.append(i)

        #st.write(phoneNumber)

        keywords = ['road', 'floor', ' st ', 'st,', 'street', ' dt ', 'district',
                'near', 'beside', 'opposite', ' at ', ' in ', 'center', 'main road',
                ' EAST ',' WEST ',' NORTH ',' SOUTH ','Nagar', 'District'
                'state','country', 'post','zip','city','zone','mandal','town','rural',
                'circle','next to','across from','area','building','towers','village',
                ' ST ',' VA ',' VA,']

        
        if any(keyword in string.lower() for keyword in keywords) or re.search(pincode_regex, string):
            address.add(string)
            addressID.append(i)
            
        # To find State and Union Territories (USING SIMILARITY SCORE)
        states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Delhi', 'Goa', 'Gujarat', 
        'Haryana','Hyderabad', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
            'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 
            'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
            "United States", "China", "Japan", "Germany", "United Kingdom", "France", "India", 
            "Canada", "Italy", "South Korea", "Russia", "Australia", "Brazil", "Spain", "Mexico", 'USA','UK']

        def string_similarity(stringOne, stringTwo):
            distance = Levenshtein.distance(stringOne, stringTwo)
            similarity = 1 - (distance / max(len(stringOne), len(stringTwo)))
            return similarity * 100
        
        for x in states:
            similarity = string_similarity(x.lower(), string.lower())
            if similarity > 50:
                addressID.add(string)
                addressID.append(i)
                
        # WEBSITE URL  
        website_regex = r"/^((https?|ftp|smtp):\/\/)?(www.)?[a-z0-9]+(\.[a-z]{2,}){1,3}(#?\/?[a-zA-Z0-9#]+)*\/?(\?[a-zA-Z0-9-_]+=[a-zA-Z0-9-%]+&?)?$/;"
        if re.match(website_regex, string):
            website = string.lower()
            webID = i 
    return [emailAddress,emailID,Pincode,PincodeID,phoneNumber,phoneID,address,addressID,website,webID]

def regex(inputText):
    
    inputArray = inputText

    regexResult = checkRegex(inputArray)

    return regexResult

    

        



