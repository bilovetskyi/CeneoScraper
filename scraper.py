import requests

# product_code = input("Please enter the product code: ")
product_code = "129910940"
print(product_code)

url = "https://www.ceneo.pl/{prodcut_code}#tab=reviews"
response = requests.get(url)
print(response.status_code)