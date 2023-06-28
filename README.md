# Business card data extraction and management with easyocr and mysql
In these various python libraries has been used such as 

## easyocr
> Easyocr is a python package used for optical character recognition
> Here it fetches text data from the given image in array format with position of the text, text and accuracy score
> From the list we are taking the text data and making it into meaningful insights to store in relational database

## regex (re)
> Regex is used analyse the extracted data using pattern matching technique
> and assign them in their desired columns like phone number, email id to display 
and store in the sql database

## Mysql
> Mysql is used to connect with Mysql DB server and store data in the database
> Here it is used to store the data, retrieve the stored records(rows) details of business card and 
update the customer business card information


### The working flow of the app
> It will take the input business card image data 
> It will use easyocr python package to extract text from the input business card image
> The extracted text data is categorised into meaningful categories with the help of regex
> When user clicked the Store in SQL Database it will store data in table format with details like
name of the company, phone number, email etc and we can retrieve the data from the stored sql database
