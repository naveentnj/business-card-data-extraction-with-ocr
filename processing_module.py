import Levenshtein
import re

def format_title(title: str):
    """
    Formats the given title with a colored box and padding
    """
    formatted_title = f"<div style='padding:10px;background-color:rgb(0, 77, 229);border-radius:10px'><h1 style='color:rgb(255, 255, 255);text-align:center;'>{title}</h1></div>"
    return formatted_title

phoneNumber= []
phoneID=[]  
address=set()
addressID=[]
emailAddress = regex_result[0]
emailID= regex_result[0]
#st.write(emailID)
Pincode=''
PincodeID=''
website=''
webID=''

def regex(result_text):
    for i, string in enumerate(result_text):   
            #st.write(string.lower())     
            
            # TO FIND EMAIL
            if re.search(r'@', string.lower()):
                emailID=string.lower()
                emailID=i
            
            # TO FIND PINCODE
            pincode_regex = r'([0-9]{3})(\s*)?([0-9]{3,4})'
            match = re.search(pincode_regex, string.lower())
            if match:
                Pincode=match.group()
                PincodeID=i

            keywords = ['road', 'floor', ' st ', 'st,', 'street', ' dt ', 'district',
                    'near', 'beside', 'opposite', ' at ', ' in ', 'center', 'main road',
                    ' EAST ',' WEST ',' NORTH ',' SOUTH ','Nagar', 'District'
                   'state','country', 'post','zip','city','zone','mandal','town','rural',
                    'circle','next to','across from','area','building','towers','village',
                    ' ST ',' VA ',' VA,']
            # Define the regular expression pattern to match six or seven continuous digits
            digit_pattern = r'\d{6,7}'
            # Check if the string contains any of the keywords or a sequence of six or seven digits
            if any(keyword in string.lower() for keyword in keywords) or re.search(digit_pattern, string):
                address.add(string)
                addressID.append(i)
                
            # TO FIND STATE (USING SIMILARITY SCORE)
            states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 
            'Haryana','Hyderabad', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
                'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 
                'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
                "United States", "China", "Japan", "Germany", "United Kingdom", "France", "India", 
                "Canada", "Italy", "South Korea", "Russia", "Australia", "Brazil", "Spain", "Mexico", 'USA','UK']

            def string_similarity(s1, s2):
                distance = Levenshtein.distance(s1, s2)
                similarity = 1 - (distance / max(len(s1), len(s2)))
                return similarity * 100
            
            for x in states:
                similarity = string_similarity(x.lower(), string.lower())
                if similarity > 50:
                    addressID.add(string)
                    AID.append(i)
                    
            # WEBSITE URL          
            if re.match(r"(?!.*@)(www|.*com$)", string):
                website=string.lower()
                webID=i 

            return [emailAddress,emailID,Pincode,PincodeID]



