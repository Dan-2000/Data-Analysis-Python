import requests
#Link for api with access key already attached
base_url =https://api.exchangeratesapi.io/v1
#Simple prompts that asks user for the date/currencies they would like converting
access_key = input("Please enter 'https://exchangeratesapi.io/' Access Key: ")
date = input("Please enter a date('YYYY-MM-DD' Or 'Latest'): ")
base = input("Convert from(Currency): ")
currency = input("Convert to(Currency): ")
quantity = float(input("what is the value of {} you would like to convert: ".format(base)))
#URL creation for 
url = base_url + "/" + date + "?access_key=" + access_key + "&base=" + base + "&symbols" + currency
response = requests.GET(url)


