import requests
class Oauth:

    def __init__(self, client_id, client_secret, access_token_url, scope):

        self.client_id = client_id

        self.client_secret = client_secret
        self.access_token_url = access_token_url
        self.scope = scope
    def generate_token(self):

        # Set the request parameters

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        data = {

            'grant_type': 'client_credentials',

            'client_id': self.client_id,

            'client_secret': self.client_secret,

            'scope': self.scope

        }




        # Send the request to obtain the access token

        response = requests.post(self.access_token_url, headers=headers, data=data)




        if response.status_code == 200:

            access_token = response.json()['access_token']

            return access_token

        else:

            print('Error generating in access token:', response.text)

            return None





client_id = 'FTS_CLIENT_APPID'

client_secret = '6057adc8-7d62-4495-a11c-bb29eb09f4b6'

access_token_url = 'https://idcs-7e6742312d274583aa0f703733016616.identity.oraclecloud.com/oauth2/v1/token'

scope = 'rgbu:merch:MFCS-STG1'




oauth_token = Oauth(client_id, client_secret,access_token_url, scope)

access_token = oauth_token.generate_token()

if access_token:

    # print('Access token:', access_token)




    def get_api_response(access_token):

        # Make sure to replace 'API_ENDPOINT' with the actual API endpoint URL

        # API_ENDPOINT = 'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/MerchIntegrations/services/foundation/item/100140000'

        API_ENDPOINT='https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/PricingServices/services/private/omnichannel/v1/item/price?pricetype=INITIAL&limit=10&item=100060021&location=11003'

    # Make the API request with the access token

        headers = {

            'Authorization': 'Bearer ' + access_token

        }




        response = requests.get(API_ENDPOINT, headers=headers)




        # Check the response status code

        if response.status_code == 200:

            # Success, return the API response

            # return response.json()
            # print('success')
            return ['API STATUS: 200 OK']

        else:
            # Error occurred

            print('Error:', response.text)

            return None




out=get_api_response(access_token)

print(out)
