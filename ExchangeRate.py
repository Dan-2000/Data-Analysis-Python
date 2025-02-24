import requests
#Link for api at it's base state
base_url ='https://api.exchangeratesapi.io/v1'
#Simple prompts that asks user for the date/currencies they would like converting
access_key = input("Please enter 'https://exchangeratesapi.io/' Access Key: ")
date = input("Please enter a date('YYYY-MM-DD' Or 'Latest'): ")
base = input("Convert from(Currency): ").upper()
currency = input("Convert to(Currency): ").upper()
quantity = float(input("what is the value of {} you would like to convert: ".format(base)))
#URL creation for the users specific parameters
url = base_url + "/" + date + "?access_key=" + access_key + "&base=" + base + "&symbols=" + currency + "&format=1"
response = requests.get(url)
#If the format for the below is incorrect, this will print the error message from json
if(response.ok is False):
    print("\nError {}:".format(response.status_code))
    print(response.json()['error'])
#If the format is accurate, this will proceed to perform the conversion of the two currencies and present the results
else:
    data = response.json()
    conversion_rate = data['rates'][currency]
    conversion = conversion_rate * quantity
    print("\n Here is the value of {0} {1} converted to {2} on this date {3} : {4}".format(quantity,base,currency,data['date'],conversion))