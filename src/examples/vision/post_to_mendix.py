import requests

def postRequest(label, score, operation):
    # defining the api-endpoint  
    API_ENDPOINT = "https://fruitninja-sandbox.mxapps.io/rest/aitrigger/v1/fruit/" + operation
    
    # your API key here 
    USER = 'googleaiy'
    PASS = 'ZE76!9@C7t#fqRgg'
  
    # your source code here 
    image = 'The image feature has not been implemented.'
  
    # data to be sent to api 
    data = {'FruitName':label, 
           'Score':str(score), 
           'Base64Image':image }
  
    # sending post request and saving response as response object
    # headers = {'Content-Type': 'application/json'}
    r = requests.post(url = API_ENDPOINT, json = data, auth = (USER, PASS))
    
    if r.status_code == requests.codes.ok:
        print('An update has been send to FruitNinja')
    else:
        print('Something went wrong while informing FruitNinja') 
        print('Content: ' + str(r.content))
    

postRequest('Banana',0.444,'add')