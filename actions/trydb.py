import configparser
import os
import shutil
import pandas as pd
from autocorrect import Speller
from cryptography.fernet import Fernet
import requests
import google.generativeai as genai
import string
import re
from googletrans import Translator, LANGUAGES
import langid
import googletrans

#spellchecker modules
# from nltk.stem import WordNetLemmatizer
# from textblob import Word
# from fuzzywuzzy import fuzz, process
# from fuzzywuzzy import fuzz
# from spellchecker import Speller
from spellchecker import SpellChecker

import requests,json,yaml,inflect
from typing import Text
# from bardapi import Bard


# lemmatizer = WordNetLemmatizer()
fuzzy_threshold = 90

class jsonConversion:
    #this array is ging to store the values from the functions, at the end of the function. it is getiting called and returned in the 
    #append_all_the_outputs()
    def __init__(self):
        # Initialize an empty list to store the results
        self.results_array = []

    def compiled_array_return(self):
        self.results_array = self.results_array
        return self.results_array


    def read_encrypted_config(self, filename):
        # Load the encrypted configuration from the file
        with open(filename, 'r') as encrypted_file:
            encrypted_config = encrypted_file.read()

        # Load the secret key from the file
        with open('secret.key', 'rb') as key_file:
            secret_key = key_file.read()

        # Create a Fernet cipher using the loaded secret key
        cipher = Fernet(secret_key)

        # Decrypt the configuration string
        decrypted_config = cipher.decrypt(encrypted_config.encode()).decode()

        return decrypted_config

    def read_client_details(self, filename):
        # Read the decrypted configuration
        decrypted_config = self.read_encrypted_config(filename)

        # Parse the configuration as INI
        config_parser = configparser.ConfigParser()
        config_parser.read_string(decrypted_config)

        # Access the client details from the [client_details] section
        client_id = config_parser.get('client_details', 'client_id')
        client_secret = config_parser.get('client_details', 'client_secret_key')
        access_token_url = config_parser.get('client_details', 'access_token_url')
        scope = config_parser.get('client_details', 'scope')

        return client_id, client_secret, access_token_url, scope

    def generate_token(self, filename):
        # Get the client details
        client_id, client_secret, access_token_url, scope = self.read_client_details(filename)

        # Set the request parameters
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': scope
        }

        # Send the request to obtain the access token
        response = requests.post(access_token_url, headers=headers, data=data)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            return access_token
        else:
            print('Error generating in access token:', response.text)
            return None
        
    # def __init__(self, client_id, client_secret, access_token_url, scope):
    #         self.client_id = client_id
    #         self.client_secret = client_secret
    #         self.access_token_url = access_token_url
    #         self.scope = scope

    # def generate_token(self):
    #     print("inside generate token")
    #     # Set the request parameters
    #     headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #     data = {
    #         'grant_type': 'client_credentials',
    #         'client_id': self.client_id,
    #         'client_secret': self.client_secret,
    #         'scope': self.scope
    #     }
    #     # Send the request to obtain the access token
    #     response = requests.post(self.access_token_url, headers=headers, data=data)
    #     if response.status_code == 200:
    #         access_token = response.json()['access_token']
    #         return access_token
    #     else:
    #         print('Error generating in access token:', response.text)
    #         return None
        
            
#     def get_api_response_usecase3(self,access_token,item_loc):
#         self.item_loc = item_loc
#         # item1=tracker.get_slot('item_loc')
#         # print()
#         # loc = input("Enter location: ")
#         API_ENDPOINT = f'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/PricingServices/services/private/omnichannel/v1/item/price?pricetype=INITIAL&item={self.item_loc}'
#         headers = {
#             'Authorization': 'Bearer ' + access_token
#         }
#         response = requests.get(API_ENDPOINT, headers=headers)
#         price_u1_details = " "
#         price_u1_data = []
#         if response.status_code == 200:
#             api_response = response.json()
#             items = api_response.get('items', [])
#             output = []

#             for item_data in items:
#                 if item_data.get('item') == item_loc:
#                     item_no = item_data.get('item')
#                     location = item_data.get('location')
#                     location_type = item_data.get('loctype')
#                     price = item_data.get('price')

#                     item_data_dict = {
#                         'Item Number': item_no,
#                         'Location': location,
#                         'Location Type': location_type,
#                         'Price': price
#                     }
#                     output.append(item_data_dict)
#                     print(f"OUTPUT PRICE U3 {output}")
#                     price_string = ", \n".join([f"{key}: {value}" for key, value in item_data_dict.items()])
#                     price_u1_details += f"\n{price_string}\n"
#                     price_u1_data.append(item_data_dict)

#                     print("NEW order_details")
#                     print(price_u1_details)
#                 if output:
# ##server code starts
#                     # df = pd.DataFrame(output)
#                     # filename = "item_prices-u3.xlsx"

#                     # # Define the directory where you want to save the file on the server
#                     # server_excel_directory = "/app/excel_files"  # Adjust this path to your server's configuration

#                     # # Ensure the directory exists
#                     # os.makedirs(server_excel_directory, exist_ok=True)

#                     # # Save the DataFrame to an Excel file in the server directory
#                     # server_filepath = os.path.join(server_excel_directory, filename)
#                     # df.to_excel(server_filepath, index=False)
                    
#                     # # # Define the server-specific downloads directory
#                     # # server_downloads_path = "/datadrive/rasa_github_new/downloads"

#                     # # # Ensure the server downloads directory exists
#                     # # os.makedirs(server_downloads_path, exist_ok=True)

#                     # # Specify the new file path in the server downloads directory
#                     # server_new_file_path = "http://20.235.145.135:7739/excel_files/item_prices-u3.xlsx"
#                     # # Move the file to the server downloads directory
#                     # # shutil.move(server_filepath, server_new_file_path)

#                     # # Get the file URL for sending to the user
#                     # file_url = server_new_file_path

#                     # return output, file_url
# ##server code ends

# ##local file starts
#                 # Create a DataFrame from the list of dictionaries
#                     df = pd.DataFrame(output)

#                     # Save the DataFrame to an Excel file
#                     filename = "item_prices-u3.xlsx"
#                     df.to_excel(filename, index=False)

#                     # Move the file to the Downloads directory (similar to previous code)
#                     file_path = os.path.join(os.getcwd(), filename)
#                     downloads_path = os.path.expanduser("~\\Downloads")
#                     # downloads_path = "/app/excel_files"
#                     new_file_path = os.path.join(downloads_path, filename)
#                     shutil.move(file_path, new_file_path)

#                     # Get the file URL for sending to the user
#                     file_url = f"file://{new_file_path}"

#                     # # return file_url  # Return the file URL for further processing
#                     return price_u1_details, file_url
# ##local file ends

#                 else:
#                     output_error = "No details exist for the given item or the number doesn't exist. You can try searching for different items."
#                     return output_error, None
#         else:
#             output_serror = "Error - Unable to fetch price details. Status code: " + str(response.status_code)
#             return output_serror, None
           
    def get_api_response_usecase3(self, access_token, item_loc):
        self.item_loc = item_loc
        print(f"item {item_loc}")

        API_ENDPOINT = f'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/PricingServices/services/private/omnichannel/v1/item/price?pricetype=INITIAL&item={self.item_loc}'
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        print("after API_ENDPOINT 1 ")
        response = requests.get(API_ENDPOINT, headers=headers)
        price_u1_details = " "
        price_u1_data = []

        # Check the response status code
        if response.status_code == 200:
            api_response = response.json()
            items = api_response.get('items', [])
            output = []

            for item_data in items:
                if item_data.get('item') == self.item_loc:
                    item_no = item_data.get('item')
                    location = item_data.get('location')
                    price = item_data.get('price')
                    item_data_dict = {
                        'Item Number': item_no,
                        'Location': location,
                        'Price': price
                    }
                    print(f"item_data_dict {item_data_dict}")
                    output.append(item_data_dict)
                    price_string = ", \n".join([f"{key}: {value}" for key, value in item_data_dict.items()])
                    price_u1_details += f"\n{price_string}\n"
                    price_u1_data.append(item_data_dict)

                    print("NEW order_details")
                    print(price_u1_details)

            if output:
                    # Create a DataFrame from the list of dictionaries
                    df = pd.DataFrame(output)

                    # Save the DataFrame to an Excel file
                    filename = "item_prices-u3.xlsx"
                    df.to_excel(filename, index=False)

                    # Move the file to the Downloads directory (similar to previous code)
                    file_path = os.path.join(os.getcwd(), filename)
                    downloads_path = os.path.expanduser("~\\Downloads")
                    # downloads_path = "/app/excel_files"
                    new_file_path = os.path.join(downloads_path, filename)
                    shutil.move(file_path, new_file_path)

                    # Get the file URL for sending to the user
                    file_url = f"file://{new_file_path}"

                    # # return file_url  # Return the file URL for further processing
                    return price_u1_details, file_url
                # df = pd.DataFrame(output)
                # filename = "item_prices-u3.xlsx"

                # # Define the directory where you want to save the file on the server
                # server_excel_directory = "/app/excel_files"  # Adjust this path to your server's configuration

                # # Ensure the directory exists
                # os.makedirs(server_excel_directory, exist_ok=True)

                # # Save the DataFrame to an Excel file in the server directory
                # server_filepath = os.path.join(server_excel_directory, filename)
                # df.to_excel(server_filepath, index=False)
                
                # server_new_file_path = "http://20.235.145.135:7739/excel_files/item_prices-u3.xlsx"
                # file_url = server_new_file_path

                # return price_u1_details, file_url
            else:
                output_error = "No details exist for the given item or location. You can try searching for different items or locations."
                return output_error, None

        else:
            output_serror = "Error - Unable to fetch price details. Status code: " + str(response.status_code)
            return output_serror, None

##local file starts 
                # # Create a DataFrame from the list of dictionaries
                #     df = pd.DataFrame(output)

                #     # Save the DataFrame to an Excel file
                #     filename = "item_prices-u3.xlsx"
                #     df.to_excel(filename, index=False)

                #     # Move the file to the Downloads directory (similar to previous code)
                #     file_path = os.path.join(os.getcwd(), filename)
                #     downloads_path = os.path.expanduser("~\\Downloads")
                #     # downloads_path = "/app/excel_files"
                #     new_file_path = os.path.join(downloads_path, filename)
                #     shutil.move(file_path, new_file_path)

                #     # Get the file URL for sending to the user
                #     file_url = f"file://{new_file_path}"

                #     # # return file_url  # Return the file URL for further processing
                #     return output, file_url
##local file ends

                

                           
    def get_api_response(self,access_token,item,loc):
        self.item=item
        self.loc=loc
        # print(self.item)
        # print(self.loc)
        # Make sure to replace 'API_ENDPOINT' with the actual API endpoint URL
        API_ENDPOINT = f'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/PricingServices/services/private/omnichannel/v1/item/price?pricetype=INITIAL&item={self.item}&location={self.loc}'
        # Make the API request with the access token
        headers = {
            'Authorization': 'Bearer ' + access_token
        }

        response = requests.get(API_ENDPOINT, headers=headers)
        price_u1_details = " "
        price_u1_data = []
        # Check the response status code
        if response.status_code == 200:
            api_response = response.json()
            # print(api_response)
            items = api_response.get('items', [])
            output=[]
            for item_data in items:
                # print("inside trydb function")
                if (item_data.get('item') == self.item and item_data.get('location')== int(self.loc)):
                    # print("Item and location match the response.")
                    item_no=item_data.get('item')
                    location=item_data.get('location')
                    # location_type=item_data.get('loctype')
                    price=item_data.get('price')
                    item_data_dict = {
                        'Item Number': item_no,
                        'Location': location,
                        'Price': price
                    }
                    output.append(item_data_dict)
                    price_string = ", \n".join([f"{key}: {value}" for key, value in item_data_dict.items()])
                    price_u1_details += f"\n{price_string}\n"
                    price_u1_data.append(item_data_dict)

                    print("NEW order_details")
                    print(price_u1_details)
            if output:
##server code starts
                # df = pd.DataFrame(output)
                # filename = "item_prices_u2.xlsx"

                # # Define the directory where you want to save the file on the server
                # server_excel_directory = "/app/excel_files"  # Adjust this path to your server's configuration

                # # Ensure the directory exists
                # os.makedirs(server_excel_directory, exist_ok=True)

                # # Save the DataFrame to an Excel file in the server directory
                # server_filepath = os.path.join(server_excel_directory, filename)
                # df.to_excel(server_filepath, index=False)
                
                # # # Define the server-specific downloads directory
                # # server_downloads_path = "/datadrive/rasa_github_new/downloads"

                # # # Ensure the server downloads directory exists
                # # os.makedirs(server_downloads_path, exist_ok=True)

                # # Specify the new file path in the server downloads directory
                # server_new_file_path = "http://20.235.145.135:7739/excel_files/item_prices_u2.xlsx"
                # # Move the file to the server downloads directory
                # # shutil.move(server_filepath, server_new_file_path)

                # # Get the file URL for sending to the user
                # file_url = server_new_file_path

                # return output, file_url
##server code ends

##local code starts 
                # Create a DataFrame from the list of dictionaries
                df = pd.DataFrame(output)

                # Save the DataFrame to an Excel file
                filename = "item_prices-u2.xlsx"
                df.to_excel(filename, index=False)

                # Move the file to the Downloads directory (similar to previous code)
                file_path = os.path.join(os.getcwd(), filename)
                downloads_path = os.path.expanduser("~\\Downloads")
                # downloads_path = "/app/excel_files"
                new_file_path = os.path.join(downloads_path, filename)
                shutil.move(file_path, new_file_path)

                # Get the file URL for sending to the user
                file_url = f"file://{new_file_path}"

                return price_u1_details, file_url
##local code ends

            else:
                output_error = "No details exist for the given item or location. You can try searching for different items or locations."
                # print("else")
                # print(output_error)
                return output_error, None

            # if output:
            #     return output
            # else:         
            #     return None
        else:
            output_serror = "Error - Unable to fetch price details. Status code: " + str(response.status_code)
            return output_serror, None
       
    def get_api_response_usecase1(self, access_token):
        # print("inside generate token")
        # Make sure to replace 'API_ENDPOINT' with the actual API endpoint URL
        API_ENDPOINT = 'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/PricingServices/services/private/omnichannel/v1/item/price?pricetype=INITIAL&limit=10'
        # Make the API request with the access token
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        response = requests.get(API_ENDPOINT, headers=headers)
        price_u1_details = " "
        price_u1_data = []
        # Check the response status code
        if response.status_code == 200:
            api_response = response.json()
            items = api_response.get('items', [])
            output=[]
            for item_data in items:
                    item_no = item_data.get('item')
                    location = item_data.get('location')
                    location_type = item_data.get('loctype')
                    price = item_data.get('price')

                    # price_u1_details += f"\nItem number : {item_no}\nLocation : {location}\n Location Type : {location_type}\n price : {price}"
                    item_data_dict = {
                        'Item Number': item_no,
                        'Location': location,
                        'Location Type': location_type,
                        'Price': price
                    }
                    output.append(item_data_dict)

                    price_string = ", \n".join([f"{key}: {value}" for key, value in item_data_dict.items()])
                    price_u1_details += f"\n{price_string}\n"
                    price_u1_data.append(item_data_dict)

                    print("NEW order_details")
                    print(price_u1_details)
            if output:
##server code ends
                # df = pd.DataFrame(output)
                # filename = "item_prices-u1.xlsx"
                
                # # Define the directory where you want to save the file on the server
                # server_excel_directory = "/app/excel_files"  # Adjust this path to your server's configuration

                # # Ensure the directory exists
                # os.makedirs(server_excel_directory, exist_ok=True)

                # # Save the DataFrame to an Excel file in the server directory
                # server_filepath = os.path.join(server_excel_directory, filename)
                # df.to_excel(server_filepath, index=False)
                
                # # # Define the server-specific downloads directory
                # # server_downloads_path = "/datadrive/rasa_github_new/downloads"

                # # # Ensure the server downloads directory exists
                # # os.makedirs(server_downloads_path, exist_ok=True)

                # # Specify the new file path in the server downloads directory
                # server_new_file_path = "http://20.235.145.135:7739/excel_files/item_prices-u1.xlsx"
                # # Move the file to the server downloads directory
                # # shutil.move(server_filepath, server_new_file_path)

                # # Get the file URL for sending to the user
                # file_url = server_new_file_path

                # return output, file_url
##server code ends

##local code starts
            #   Create a DataFrame from the list of dictionaries
                df = pd.DataFrame(output)

                # Save the DataFrame to an Excel file
                filename = "item_prices-u1.xlsx"
                df.to_excel(filename, index=False)

                # Move the file to the Downloads directory (similar to previous code)
                file_path = os.path.join(os.getcwd(), filename)
                downloads_path = os.path.expanduser("~\\Downloads")
                # downloads_path = "/app/excel_files"
                new_file_path = os.path.join(downloads_path, filename)
                shutil.move(file_path, new_file_path)

                # Get the file URL for sending to the user
                file_url = f"file://{new_file_path}"

                # # return file_url  # Return the file URL for further processing
                return price_u1_details, file_url
##local code ends
            else:
                output_error = "No details exist for the given item. You can try searching for different items."
                return output_error , None
        else:
            output_serror = "Error - Unable to fetch price details. Status code: " + str(response.status_code)
            return output_serror, None

    
    def order_details(self, orderno, access_token):
        self. orderno = orderno
        API_ENDPOINT = f'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/RmsReSTServices/services/private/Po/poDetail?orderNumber={orderno}'
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        response = requests.get(API_ENDPOINT, headers=headers)
        print(f"response from order {response}")
        order_data = []
        if response.status_code == 200:
            api_response = response.json()
# ------------
            for order in api_response:
                order_no = order['orderNo']
                order_details_string = f"Order Number: {order_no}\n"
                for item in order['poItemTbl']:
                    order_details = {
                        # 'Order Number': order_no,
                        'Item': item['item'],
                        'Location': item['location'],
                        'Location Type': item['locType'],
                        'Quantity Ordered': item['qtyOrdered'],
                        'Quantity Received': item['qtyReceived'],
                        'Unit Cost': item['unitCost']
                    }
                    order_string = ", \n".join([f"{key}: {value}" for key, value in order_details.items()])
                    order_details_string += f"\n{order_string}\n"
                    order_data.append(order_details)

                print("NEW order_details")
                print(order_details_string)

            if order_data:
             # uncomment  the below code for local xslx file download
                #   Create a DataFrame from the list of dictionaries
                    df = pd.DataFrame(order_data)

                    # Save the DataFrame to an Excel file
                    filename = "order_info.xlsx"
                    df.to_excel(filename, index=False)

                    # Move the file to the Downloads directory (similar to previous code)
                    file_path = os.path.join(os.getcwd(), filename)
                    print(f"file path in local {file_path}")
                    current_directory = os.getcwd()
                    print("Current Working Directory:", current_directory)
                    downloads_path = os.path.expanduser("~\\Downloads")
                    # downloads_path = "/app/excel_files"
                    new_file_path = os.path.join(downloads_path, filename)
                    shutil.move(file_path, new_file_path)

                    # Get the file URL for sending to the user
                    file_url = f"file://{new_file_path}"

                    return order_details_string, file_url
            # # uncomment  the below code for server xslx file download
            #         df = pd.DataFrame(order_data)
            #         filename = "order_info.xlsx"

            #         # Define the directory where you want to save the file on the server
            #         server_excel_directory = "/app/excel_files"  # Adjust this path to your server's configuration

            #         # Ensure the directory exists
            #         os.makedirs(server_excel_directory, exist_ok=True)

            #         # Save the DataFrame to an Excel file in the server directory
            #         server_filepath = os.path.join(server_excel_directory, filename)
            #         df.to_excel(server_filepath, index=False)
                    
            #         # # Define the server-specific downloads directory
            #         # server_downloads_path = "/datadrive/rasa_github_new/downloads"

            #         # # Ensure the server downloads directory exists
            #         # os.makedirs(server_downloads_path, exist_ok=True)

            #         # Specify the new file path in the server downloads directory
            #         server_new_file_path = "http://20.235.145.135:7739/excel_files/order_info.xlsx"
            #         # Move the file to the server downloads directory
            #         # shutil.move(server_filepath, server_new_file_path)

            #         # Get the file URL for sending to the user
            #         file_url = server_new_file_path


            #         return order_details_string, file_url              
            
        else:
            print("Error - Unable to fetch order details:", response.status_code)
            return None, None
            # for order in api_response:
            #     order_no = order['orderNo']
            #     for item in order['poItemTbl']:
            #         item_details = {
            #             'orderNo': order_no,
            #             'item': item['item'],
            #             'location': item['location'],
            #             'locType': item['locType'],
            #             'qtyOrdered': item['qtyOrdered'],
            #             'qtyReceived': item['qtyReceived'],
            #             'unitCost': item['unitCost']
            #         }
            #         print(" NEW order_details")
            #         print(item_details)
    #  -----------
                #contains the json response. print to check the api value
                # Accessing the order items and their values
#                 order_items = api_response[0]['poItemTbl']
#                 output= []
#                 order_details_list = [] 
#                 # Printing the values for each item
#                 if not order_items:  # Check if "poItemTbl" is empty
#                     print("No 'poItemTbl' found in the API response or it is empty.")
#                     return None, None

#                 for ord_det in order_items:
#                     # Item=ord_det["item"]
#                     Item=ord_det.get('item')
#                     location=ord_det.get('location')
#                     location_type=ord_det.get('locType')
#                     qtyOrdered=ord_det.get('qtyOrdered')
#                     qtyReceived=ord_det.get('qtyReceived')
#                     unitCost=ord_det.get('unitCost')

#                     order_item_data = {
#                         'Item Number': Item,
#                         'Location': location,
#                         'Location Type': location_type,
#                         'Quantity Ordered': qtyOrdered,
#                         'Quantity Received': qtyReceived,
#                         'Unit Cost': unitCost
#                     }


#                     output.append(order_item_data)

#                     data = ""  # Initialize an empty string

#                 # Iterate through each order item data
#                 for order_item_data in output:
#                     data += (
#                         f"Item Number: {order_item_data['Item Number']}\n"
#                         f"Location: {order_item_data['Location']}\n"
#                         f"Location Type: {order_item_data['Location Type']}\n"
#                         f"Quantity Ordered: {order_item_data['Quantity Ordered']}\n"
#                         f"Quantity Received: {order_item_data['Quantity Received']}\n"
#                         f"Unit Cost: {order_item_data['Unit Cost']}\n"
#                     )

#                 # print(data)
#                 # Create a dictionary for each order detail and append it to the list
                

#                 if output:
                    
    #server code starts
    # Create a DataFrame from the list of dictionaries

#     ##server code ends
#     ##local code starts
#                 #   Create a DataFrame from the list of dictionaries
#                     df = pd.DataFrame(output)

#                     # Save the DataFrame to an Excel file
#                     filename = "order_info.xlsx"
#                     df.to_excel(filename, index=False)

#                     # Move the file to the Downloads directory (similar to previous code)
#                     file_path = os.path.join(os.getcwd(), filename)
#                     print(f"file path in local {file_path}")
#                     current_directory = os.getcwd()
#                     print("Current Working Directory:", current_directory)
#                     downloads_path = os.path.expanduser("~\\Downloads")
#                     # downloads_path = "/app/excel_files"
#                     new_file_path = os.path.join(downloads_path, filename)
#                     shutil.move(file_path, new_file_path)

#                     # Get the file URL for sending to the user
#                     file_url = f"file://{new_file_path}"

#                     return order_details_string, file_url
# ##local code ends

#         else:
#             print("Error - Unable to fetch order details:", response.status_code)
#             return None, None

    # def inventory_details_for_store(self, loc, loc_type, access_token):
    #     self.loc = loc
    #     self.loc_type = loc_type
    #     API_ENDPOINT = f'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/MerchIntegrations/services/inventory/available?location={self.loc}&locationType={self.loc_type}'
    #     headers = {
    #         'Authorization': 'Bearer ' + access_token
    #     }
    #     response = requests.get(API_ENDPOINT, headers=headers)  

    #     if response.status_code == 200:
    #         api_response = response.json()
    #         # print(api_response)
    #         items = api_response.get('items', [])
    #         # print(items)
    #         output= []
    #         for item_data in items:
    #             # print("Item and location match the response.")
    #             item_no=item_data.get('item')
    #             location=item_data.get('location')
    #             location_type=item_data.get('locationType')
    #             soh=item_data.get('stockOnHand')
    #             # output += f"\nitem_no: {item_no}\n"
    #             # output += f"location: {location}\n"
    #             # output += f"location_type: {location_type}\n"
    #             # output += f"stock on hand: {soh}\n\n"
    #             # self.results_array.append(output)
    #             # # print(f"inside inventory array - s: {self.results_array}")
    #             inventory_for_store = {
    #                 'Item No': item_no,
    #                 'Location': location,
    #                 'Location Type': location_type,
    #                 'Stock On Hand': soh
                    
    #             }
    #             output.append(inventory_for_store)

    #         if inventory_for_store:
    #             print("inside if")
    #             # Create a DataFrame from the list of dictionaries
    #             df = pd.DataFrame(output)
    #             # Save the DataFrame to an Excel file
    #             filename = "inventory_for_store.xlsx"
    #             df.to_excel(filename, index=False)

    #             # Move the file to the Downloads directory (similar to previous code)
    #             file_path = os.path.join(os.getcwd(), filename)
    #             downloads_path = os.path.expanduser("~\\Downloads")
    #             # downloads_path = "/app/excel_files"
    #             new_file_path = os.path.join(downloads_path, filename)
    #             shutil.move(file_path, new_file_path)

    #             # Get the file URL for sending to the user
    #             file_url = f"file://{new_file_path}"
                
    #             return inventory_for_store, file_url

    #         else:
    #             print("inside else")

    #             print("Error - Unable to fetch inventory details:", response.status_code)
    #             return None, None

    def inventory_details_for_store(self, loc, loc_type, access_token):
        self.loc = loc
        self.loc_type = loc_type
        API_ENDPOINT = f'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/MerchIntegrations/services/inventory/available?location={self.loc}&locationType={self.loc_type}'
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        response = requests.get(API_ENDPOINT, headers=headers)
        
        if response.status_code == 200:
            inventory_data = []
            inventory_details_string = ''
            api_response = response.json()
            items = api_response.get('items', [])
            output = []
            for item_data in items:
                item_no = item_data.get('item')
                location = item_data.get('location')
                location_type = item_data.get('locationType')
                soh = item_data.get('stockOnHand')


                item_info = {
                    'Item No': item_no,
                    'Location': location,
                    'Location Type': location_type,
                    'Stock on Hand': soh
                }

                output.append(item_info)
# 
                inventory_string = ", \n".join([f"{key}: {value}" for key, value in item_info.items()])
                inventory_details_string += f"\n{inventory_string}\n"
                inventory_data.append(inventory_details_string)

                print("NEW inventory_details")
                print(inventory_details_string)
# 
                

            if output:
##server code starts
                # df = pd.DataFrame(output)
                # filename = "inventory_for_store.xlsx"

                # # Define the directory where you want to save the file on the server
                # server_excel_directory = "/app/excel_files"  # Adjust this path to your server's configuration

                # # Ensure the directory exists
                # os.makedirs(server_excel_directory, exist_ok=True)

                # # Save the DataFrame to an Excel file in the server directory
                # server_filepath = os.path.join(server_excel_directory, filename)
                # df.to_excel(server_filepath, index=False)
                
                # # # Define the server-specific downloads directory
                # # server_downloads_path = "/datadrive/rasa_github_new/downloads"

                # # # Ensure the server downloads directory exists
                # # os.makedirs(server_downloads_path, exist_ok=True)

                # # Specify the new file path in the server downloads directory
                # server_new_file_path = "http://20.235.145.135:7739/excel_files/inventory_for_store.xlsx"
                # # Move the file to the server downloads directory
                # # shutil.move(server_filepath, server_new_file_path)

                # # Get the file URL for sending to the user
                # file_url = server_new_file_path
                # return output, file_url
            
##server code ends
##local code starts

                # Create a DataFrame from the list of dictionaries
                df = pd.DataFrame(output)

                # Save the DataFrame to an Excel file
                filename = "inventory_for_store.xlsx"
                df.to_excel(filename, index=False)

                # Move the file to the Downloads directory (similar to previous code)
                file_path = os.path.join(os.getcwd(), filename)
                downloads_path = os.path.expanduser("~\\Downloads")
                # downloads_path = "/app/excel_files"
                new_file_path = os.path.join(downloads_path, filename)
                shutil.move(file_path, new_file_path)

                # Get the file URL for sending to the user
                file_url = f"file://{new_file_path}"
                return inventory_details_string, file_url
# #local code ends

            else:
                print('No inventory items found.')
                return None, None
        else:
            print('Error:', response.status_code)
            return None, None
        
    def inventory_details_for_wh(self, loc, loc_type, access_token):
        self.loc = loc
        self.loc_type = loc_type
        API_ENDPOINT = f'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/MerchIntegrations/services/inventory/available?location={self.loc}&locationType={self.loc_type}'
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        response = requests.get(API_ENDPOINT, headers=headers)

        if response.status_code == 200:
            inventory_data = []
            inventory_details_string = ''
            api_response = response.json()
            items = api_response.get('items', [])
            output = []
            for item_data in items:
                item_no = item_data.get('item')
                location = item_data.get('location')
                location_type = item_data.get('locationType')
                soh = item_data.get('stockOnHand')


                item_info = {
                    'Item No': item_no,
                    'Location': location,
                    'Location Type': location_type,
                    'Stock on Hand': soh
                }

                output.append(item_info)
# 
                inventory_string = ", \n".join([f"{key}: {value}" for key, value in item_info.items()])
                inventory_details_string += f"\n{inventory_string}\n"
                inventory_data.append(inventory_details_string)

                print("NEW inventory_details")
                print(inventory_details_string)
# 
            if output:
        # if response.status_code == 200:
        #     api_response = response.json()
        #     # print(api_response)
        #     items = api_response.get('items', [])
        #     # print(items)
        #     output= []
        #     for item_data in items:
        #         # print("Item and location match the response.")
        #         item_no=item_data.get('item')
        #         location=item_data.get('location')
        #         location_type=item_data.get('locationType')
        #         soh=item_data.get('stockOnHand')
        #         # output += f"\nitem_no: {item_no}\n"
        #         # output += f"location: {location}\n"
        #         # output += f"location_type: {location_type}\n"
        #         # output += f"stock on hand: {soh}\n\n"
        #         # self.results_array.append(output)
        #         # print(f"inside wh: {self.results_array}")
        #         inventory_for_wh = {
        #             'Item No': item_no,
        #             'Location': location,
        #             'Location Type': location_type,
        #             'Stock On Hand': soh
        #         }
        #         output.append(inventory_for_wh)

# ##server code starts
                # df = pd.DataFrame(output)
                # filename = "inventory_for_wh.xlsx"

                # # Define the directory where you want to save the file on the server
                # server_excel_directory = "/app/excel_files"  # Adjust this path to your server's configuration

                # # Ensure the directory exists
                # os.makedirs(server_excel_directory, exist_ok=True)

                # # Save the DataFrame to an Excel file in the server directory
                # server_filepath = os.path.join(server_excel_directory, filename)
                # df.to_excel(server_filepath, index=False)
                
                # # # Define the server-specific downloads directory
                # # server_downloads_path = "/datadrive/rasa_github_new/downloads"

                # # # Ensure the server downloads directory exists
                # # os.makedirs(server_downloads_path, exist_ok=True)

                # # Specify the new file path in the server downloads directory
                # server_new_file_path = "http://20.235.145.135:7739/excel_files/inventory_for_wh.xlsx"
                # # Move the file to the server downloads directory
                # # shutil.move(server_filepath, server_new_file_path)

                # # Get the file URL for sending to the user
                # file_url = server_new_file_path
                # return output, file_url
##server code ends

##local code starts
                # Create a DataFrame from the list of dictionaries
                df = pd.DataFrame(output)

                # Save the DataFrame to an Excel file
                filename = "inventory_for_wh.xlsx"
                df.to_excel(filename, index=False)

                # Move the file to the Downloads directory (similar to previous code)
                file_path = os.path.join(os.getcwd(), filename)
                downloads_path = os.path.expanduser("~\\Downloads")
                # downloads_path = "/app/excel_files"
                new_file_path = os.path.join(downloads_path, filename)
                shutil.move(file_path, new_file_path)

                # Get the file URL for sending to the user
                file_url = f"file://{new_file_path}"
                return inventory_details_string, file_url
##local code ends
            else:
                print('No inventory items found.')
                return None, None
        else:
            print('Error:', response.status_code)
            return None, None

    def supplier_details(self, supplier_no, access_token):
        self.supplier_no = supplier_no

        # API endpoint URL with the supplier number as a parameter
        API_ENDPOINT = f'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/RmsReSTServices/services/private/Supplier/supplierDetail?supplierNumber={self.supplier_no}'

        # Make the API request with the access token
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        supplier_details =''
        response = requests.get(API_ENDPOINT, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            api_response = response.json()

            # Extracting required fields from the API response
            supplier = api_response[0]['supplier']
            supName = api_response[0]['supName']
            currencyCode = api_response[0]['currencyCode']
            vatRegion = api_response[0]['vatRegion']
            freight_terms = api_response[0]['freightTerms']
            supplier_details += f"Supplier: {supplier}\nSupplier Name: {supName}\nCurrency Code: {currencyCode}\nVAT Region: {vatRegion}\nFreight_terms: {freight_terms}"

            supplier_data = {
                'Supplier': supplier,
                'Supplier Name': supName,
                'Currency Code': currencyCode,
                'VAT Region': vatRegion,
                'Freight Terms': freight_terms
            }
            if supplier_data:
# #server start
                # df = pd.DataFrame([supplier_data])
                # filename = "supplier_info.xlsx"

                # # Define the directory where you want to save the file on the server
                # server_excel_directory = "/app/excel_files"  # Adjust this path to your server's configuration

                # # Ensure the directory exists
                # os.makedirs(server_excel_directory, exist_ok=True)

                # # Save the DataFrame to an Excel file in the server directory
                # server_filepath = os.path.join(server_excel_directory, filename)
                # df.to_excel(server_filepath, index=False)
                
                # # Specify the new file path in the server downloads directory
                # server_new_file_path = f"http://20.235.145.135:7739/excel_files/supplier_info.xlsx"

                # # Get the file URL for sending to the user
                # file_url = server_new_file_path
                # return supplier_details, file_url
# #server ends
# #local starts
                # Create a DataFrame from the list of dictionaries
                df = pd.DataFrame([supplier_data])

                # Save the DataFrame to an Excel file
                filename = "supplier_info.xlsx"
                df.to_excel(filename, index=False)

                # Move the file to the Downloads directory (similar to previous code)
                file_path = os.path.join(os.getcwd(), filename)
                print(f"file path in local {file_path}")
                downloads_path = os.path.expanduser("~\\Downloads")
                # downloads_path = "/app/excel_files"
                new_file_path = os.path.join(downloads_path, filename)
                shutil.move(file_path, new_file_path)

                # Get the file URL for sending to the user
                file_url = f"file://{new_file_path}"

                return supplier_details, file_url
# # local ends

  
        else:
            print("Failed to get API response. Status Code:", response.status_code)
            return None, None
        
    def item_details(self, item_no, access_token):
        self.item_no = item_no
        print(f"item number",item_no)
        API_ENDPOINT = f'https://rex.retail.eu-frankfurt-1.ocs.oraclecloud.com/rgbu-rex-appa-stg1-mfcs/RmsReSTServices/services/private/Item/itemDetail?item={self.item_no}'

        # Make the API request with the access token
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        item_details = ''
        response = requests.get(API_ENDPOINT, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            api_response = response.json()
            # Extracting required fields from the API response
            itemGrandparent = api_response[0]['itemGrandparent']
            itemParent = api_response[0]['itemParent']
            item = api_response[0]['item']
            itemDesc = api_response[0]['itemDesc']
            status = api_response[0]['status']
            itemLevel = api_response[0]['itemLevel']
            tranLevel = api_response[0]['tranLevel']
            
            item_details += f"item Grandparent : {itemGrandparent} \nitem Parent : {itemParent}\n item : {item}\n item Description : {itemDesc}\n status : {status}\n item Level : {itemLevel}\n tran Level : {tranLevel}"

            item_data = {
                'itemGrandparent ': itemGrandparent,
                'itemParent ': itemParent,
                'item ': item,
                'itemDesc ': itemDesc,
                'status ': status,
                'itemLevel ': itemLevel,
                'tranLevel ': tranLevel

            }
            if item_data:
# #local code starts
                # Create a DataFrame from the list of dictionaries
                df = pd.DataFrame([item_data])
                # Save the DataFrame to an Excel file
                filename = "item_info.xlsx"
                df.to_excel(filename, index=False)
                # Move the file to the Downloads directory (similar to previous code)
                file_path = os.path.join(os.getcwd(), filename)
                downloads_path = os.path.expanduser("~\\Downloads")
                new_file_path = os.path.join(downloads_path, filename)
                shutil.move(file_path, new_file_path)
                # Get the file URL for sending to the user
                file_url = f"file://{new_file_path}"
                return item_details, file_url
# #local code ends

#  # server code start
                # df = pd.DataFrame([item_data])
                # filename = "item_info.xlsx"
                # # Define the directory where you want to save the file on the server
                # server_excel_directory = "/app/excel_files"  # Adjust this path to your server's configuration
                # # Ensure the directory exists
                # os.makedirs(server_excel_directory, exist_ok=True)
                # # Save the DataFrame to an Excel file in the server directory
                # server_filepath = os.path.join(server_excel_directory, filename)
                # df.to_excel(server_filepath, index=False)
                # # Specify the new file path in the server downloads directory
                # server_new_file_path = "http://20.235.145.135:7739/excel_files/item_info.xlsx"
                # # Get the file URL for sending to the user
                # file_url = server_new_file_path
                # return item_data, file_url
#  # server code ends

        else:
            print("Failed to get API response. Status Code:", response.status_code)
            return None, None

# -------------------------------------------------------------------------------------------------------
    
class allFunc:
    key_of_lang = None  # Declare the global class variable
    # def __init__(self):
    #     self.key_of_lang = None  # Initialize key_of_lang attribute
    #     print(f"inside init key_of_lang {self.key_of_lang}")


    # def set_key_of_lang(self, language):
    #     self.key_of_lang = language
    #     print(f"After setting lang {self.key_of_lang}")
    #     return self.key_of_lang



#     def call_chatgpt_api(self, user_input: Text) -> Text:
#         os.environ['_BARD_API_KEY']="ZAhJrc70j0DiIfw7J_wQnuD3QLzpIkMWyFicPcnQGkXMMF6aFnAz2CAUmA22ACMw_sTu2A."
#         answer = Bard().get_answer(user_input)['content']
#         return answer
#      #new -ZAiGpSg0uIH2xwPGnYn2oL-rON6OjZ5urmtqeesnALQX6PYi6x1sWTp6iqNWO7ANGpQySA.
#   #old - YwiGpT53EGvjiLA9g2QGpH0TUnQwqLCo110s3WYpPsXJVqKcGKvujc1VX5QJZayTIXAHqA.
    def palmApi(self, user_input: Text) -> Text:
        API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key=AIzaSyDSWNlyibcYAk-ivUIrlDrzz3S4BJr236E"
        print(" ******************* ")
        print(f"{user_input}")
        headers = {
        'Content-Type': 'application/json'
        }
        # user_input = 'tell me about bts'
        # Create the request data with the user input
        request_data = {
            "prompt": {
                "text": user_input
            }
        }
        # Convert the request_data to a JSON string
        request_json = json.dumps(request_data)
        
        # Make a POST request with the user input in the request body
        response = requests.post(API_ENDPOINT, headers=headers, data=request_json)
        
        if response.status_code == 200:
            palmapi_response = response.json()
            output_text = palmapi_response['candidates'][0]['output']

            print(output_text)
            return output_text
        else:
            return None

    def checking_other_intents(self, keyword):
        # Specify the path to the NLU training data YAML file
        nlu_file_path=r"C:\Users\yraja\LogicBot\local_test\data\nlu.yml"
        # nlu_file_path="/app/data/nlu.yml"

        # Load the NLU training data from the YAML file
        with open(nlu_file_path, "r") as file:
            nlu_data = yaml.safe_load(file)

        examples = []
        
        other_intents = ["domain_details","get_item_all_locs","get_item_prices","ask_botname","ask_howold","ask_howbuilt","ask_time","ask_weather",
                            "get_specific_price","goodbye","question_intent","nlu_fallback_math_operations","affirm",
                            "session_start_without_reloading","user_query","get_more_info",
                            "user_entered_numeric_values","inventory_loc", "get_inv_loc"]
        res = []
        matched_intents = []  # Store matching intents
        intent1 = None
        # Iterate through all intents in the NLU data
        if "nlu" in nlu_data:
            for intent_data in nlu_data["nlu"]:
                if isinstance(intent_data, dict):
                    intent = intent_data.get("intent")
                    # Exclude "domain_details" and "question_intent" intents
                    #can mention intents that we only need - but it will run the other intents if these words are mentioned.
                    #good to mention not in intents                  
                    if intent not in other_intents:
                        print(f"picked other intetnes: {intent}")
                        examples_str = intent_data.get("examples", "")
                        examples = examples_str.split("\n")
                        # print(f"exstr: {examples}")
                        #   # Remove hyphens from the examples
                        examples = [example.replace("- ", "") for example in examples]

                        # stemmed_examples = []
                        # for example in examples:
                        #     stemmed_words = [stemmer.stem(word) for word in example.split()]
                        #     stemmed_examples.append(' '.join(stemmed_words))
                        
                        print(f"other examples:{examples}") 
                        result = self.check_words_in_intent(keyword, examples)
                        # print(f"printing the result:{result}")
 
                        for r in result:
                            # print(f"r: {r}")
                            if r==True:
                                # intent1=intent
                                matched_intents.append(intent)  # Append matching intent

                        res.extend(result)    
                            

                        # for r in result:
                        #     print(f"r: {r}")
                        #     if r==True:
                        #         intent_names.append(intent)  
                        #         intent1= intent_names
                        # res.extend(result)            
        return res, matched_intents
    
    def check_words_in_intent(self, user_input, intent_examples):
        # print(f"check1 {user_input} ,{intent_examples}")
        unwanted_words = [
                            "info","is", "the", "was", "but", "yet", "and", "or", "not", "are", "were","hows","do?","please",
                            "if", "then", "that", "this", "there", "these", "those", "with", "ai","able",
                            "without", "in", "on", "at", "to", "from", "for", "by", "as", "of","whos",
                            "a", "an", "be", "been", "being", "has", "have", "had", "do",
                            "does", "did", "can", "could", "should", "would", "may", "might",
                            "must", "shall", "will", "i", "you", "he", "she", "it", "we", "they", "KFC",
                            "his", "her", "its", "our", "their", "mine","PLEASE","tell",
                            "hers", "ours", "theirs","to","want","know","about", "abou","knwo","no","yes","ya","good","bad",
                            'weren', 'their', 'doing', 'all', 'were', "you've", 'she', 'those', 'not', 'how', 'from', 'that', 'own', 'because', 'very', "that'll", 'ours', "needn't", 'had', 'should', "hadn't", 'under', 'are', 'where', "haven't", 'or', 'shouldn', 'here', "wouldn't", 're', 'off', 'hadn', 'which', 'as', 'why', 'having', 'same', 'through', 've', 'won', 'themselves', 'and', 'our', 'between', 'into', 'of', 'yourselves', 'but', 'wasn', 'theirs', 'up', 'aren', 'me', 'before', 'than', 'with', 'such', 'by', 'until', 'further', 'down', 'can', 'they', 'yourself', 'doesn', 'hers', 'some', 'needn', 'ma', "should've", 'it', 'couldn', 'hasn', 'will', 'what', 'below', 'we', 'other', 'haven', 'now', 'no', "shan't", 'if', 'the', 'himself', 'once', 'mustn', 'its', "couldn't", 'for', 'didn', 'i', 'at', 'on', 'out', 'him', 'only', 'herself', 'so', 's', 'them', "you're", 'have', 'wouldn', 'after', 'don', 'few', 'll', 'then', 'you', 'her', 'nor', 'his', 'who', 'mightn', 'y', "mustn't", 'any', 'myself', 'to', 'itself', 'been', "it's", 't', "doesn't", 'he', 'am', 'being', 'too', 'ain', 'about', 'during', 'against', "wasn't", "mightn't", 'most', 'was', 'in', 'there', "she's", 'above', "won't", 'shan', 'ourselves', 'does', 'did', 'whom', 'do', 'is', "you'd", 'be', 
                            'has', 'when', 'isn', "you'll", "didn't", 'each', "don't", 'a', 'this', 'over', 'm', 'o', 'd', "aren't", 'again', 'more', "weren't", 'both', 
                            'just', "isn't", "shouldn't", "hasn't", 'while', 'these', 'an', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
                        ]
            # Convert user input to lowercase and remove common words
        user_input = ' '.join([word for word in user_input.lower().split() if word not in unwanted_words])

        # Convert intent examples to lowercase and remove empty strings
        intent_examples = [example.lower() for example in intent_examples if example]
        user_words = user_input.split()
        # "Inventory Check Stock Take Audit Count Verification Control Reconciliation Inspection Monitoring Tracking Management."
        #words in quotation comes like this and s a whole, is considered as a
        print(f"user ipt words : {user_words}")
        # List to store matched words and their positions
        matched_words = []
        res = []
        #THIS CODE WILL TAKE THE PLURAL FORMS INTO CONSIDERATION - ENABLE THIS PART IF NEEDED
        # Check if any word matches the intent examples
                            
        for word in user_words:
            plural_form=self.check_plural(word)
            # corrected_word = self.correct_spelling(word)
            spell = Speller(lang='en')
            corrected_word = spell(word)
            found = False
            for position, words in enumerate(intent_examples):
                
                if word in words:
                # if word in words or corrected_word in words or any(fuzz.ratio(word, w) >= fuzzy_threshold for w in words):
                    if len(word) > 2 and word != 'po' and word != 'PO':
                        print(f"IF - Match found! Word: {word}, Position: {position}")
                        matched_words.append((word, position))
                        found = True
                        break
                # elif plural_form in words:
                #     print(f"ELIF - plural Match found! Word: {word}, Position: {position}")
                #     matched_words.append((word, position))
                #     found = True
                #     break
                #if plural form is not there, then it is checking the misspelled word here. the misspelled word can also e a plural form, so check both
                # If the word is not found as is or in plural form,
                # try correcting the misspelled word and check agains

                elif corrected_word in words:
                    print(f"ELSE - Corrected Match found! Word: {corrected_word}, Position: {position}")
                    matched_words.append((corrected_word, position))
                    found = True
                    if corrected_word in unwanted_words:
                        found = False

            res.append(found)  # Append True if the word is found, False otherwise
        
#ANOTHER METHOD - WORKS FINE - NLTK MODULE INSTALLATION ERROR OCCURED, SO USING INFLECT MODULE
        # for word in user_words:
        #     #incase if user enters a misspelled word, it is corrected(rasa has the inbuilt property, but it is not working for all cases - ex: ietm)
        #     self.correct_word_spelling(word)
        #     found = False
        #     for position, example in enumerate(intent_examples):
        #         example_words = example.split()
        #         preprocessed_words = [lemmatizer.lemmatize(w.lower()) for w in example_words]
                
        #         if word in preprocessed_words or any(fuzz.ratio(word, w) >= fuzzy_threshold for w in preprocessed_words):
        #             matched_words.append((word, position))
        #             found = True
        #             break

        #     res.append(found)  # Append True if the word is found, False otherwise
        #     print(res)

#THIS CODE WILL NOT TAKE THE PLURAL FORMS INTO CONSIDERATION - ENABLE THIS PART IF NEEDED
        # for word in user_words:
        #     found = False
        #     for position, words in enumerate(intent_examples):
        #         if word in words:
        #             print(f"Match found! Word: {word}, Position: {position}")
        #             matched_words.append((word, position))
        #             found = True
        #             break
            
        #     res.append(found)  # Append True if the word is found, False otherwise

        if matched_words:
            print(f"Matched words: {matched_words}")
        return res
#--------------------------------------------------------
    def remove_punctuation(self, word_list):
        # Remove punctuation from words in the list and convert to lowercase
        table = str.maketrans('', '', string.punctuation)
        cleaned_words = [word.translate(table).lower() for word in word_list]
        return cleaned_words

    def check_for_synonym_keywords(self, word_list):

        supplier_keywords = ['Supplier','vendor']
        order_keyword = ['order','Order'] # ,'purchase order'
        inventory_keywords = ['Inventory','inventory','stock']
        pricing_keywords = [ 'Price', 'Prices'] # 'cost'
        item_keywords = [ 'item', 'Items']


        supplier_keywords_lower = [word.lower() for word in supplier_keywords]
        order_keyword_lower = [word.lower() for word in order_keyword]
        inventory_keywords_lower = [word.lower() for word in inventory_keywords]
        pricing_keywords_lower = [word.lower() for word in pricing_keywords]
        item_keywords_lower = [word.lower() for word in item_keywords]


        
      # Compile regular expressions
        supplier_regex = re.compile('|'.join(supplier_keywords_lower), re.IGNORECASE)
        order_regex = re.compile('|'.join(order_keyword_lower), re.IGNORECASE)
        inventory_regex = re.compile('|'.join(inventory_keywords_lower), re.IGNORECASE)
        pricing_regex = re.compile('|'.join(pricing_keywords_lower), re.IGNORECASE)
        item_regex = re.compile('|'.join(item_keywords_lower), re.IGNORECASE)


        # all_keywords_pattern = '|'.join(supplier_keywords_lower + order_keyword_lower + inventory_keywords_lower + pricing_keywords_lower)
        # print(f"all_keywords_pattern-{all_keywords_pattern}")
        # keywords_regex = re.compile(all_keywords_pattern, re.IGNORECASE)

        # print(f"keywords_regex-{keywords_regex}")

        # inventory_keywords = ['Inventory', 'Stock', 'Stocks', 'Stocktaking', 'Stocktake', 'Stock control', 'Stock check', 'Stock count', 'Stock level', 'Stock management', 'Stockroom']
        # pricing_keywords = ['Pricing', 'Price', 'Prices', 'Pricelist', 'Price list', 'Pricing strategy', 'Price management', 'Pricing policy', 'Pricing model', 'Price range']
        # matched_categories = []

        found_keywords = []

        # print(f"word list {word_list}")
        cleaned_words = self.remove_punctuation(word_list)
        print(f"cleaned_words {cleaned_words}")

        

            
# -------------------
        found_keywords = {
            "supplier": [],
            "order": [],
            "inventory": [],
            "pricing": [],
            "item": [],
        }


        for word in cleaned_words:
            if supplier_regex.search(word):
                found_keywords["supplier"].append(word)
            elif order_regex.search(word):
                found_keywords["order"].append(word)
            elif inventory_regex.search(word):
                found_keywords["inventory"].append(word)
            elif pricing_regex.search(word):
                found_keywords["pricing"].append(word)
            elif item_regex.search(word):
                 if word.lower() != "itemized statement":  # Check for the removed word
                    found_keywords["item"].append(word)               

        if found_keywords:
            # Print counts for each category
            for category, words in found_keywords.items():
                print(f"Words found in {category} category: {words}")
                

        # # Check for multiple categories with non-zero counts
        # non_zero_categories = [category for category, words in found_keywords.items() if len(words) > 0]
        # if len(non_zero_categories) > 1:
        #     print("It seems your query falls under multiple categories. Please rephrase your statement.")
        #     # Print the categories with non-zero counts
        #     for category in non_zero_categories:
        #         print(f"Category '{category}' has non-zero count.")
        #     # Return a list containing the counts for each category
        #     return [len(words) for words in found_keywords.values()]
        
        # elif len(non_zero_categories) == 1:
        #     # Return the words for the single category
        #     single_category = non_zero_categories[0]
        #     print(f"Words found in {single_category} category: {found_keywords[single_category]}")
        #     return found_keywords[single_category]
        # else:
        #     print("No matching categories found.")
        #     return []
            # Check for multiple categories
            

            result = [len(words) for words in found_keywords.values()]

            # Check if all values in result are zero
            if all(count == 0 for count in result):
                print("No category identified.")
                print(f"result - {result}")
                no_category = "none"
                return no_category

            # Count non-zero elements in the result
            non_zero_count = sum(count > 0 for count in result)  # Count directly using a generator expression

            if non_zero_count == 1:
                # Print the single category message
                category_with_match = next(category for category, count in zip(found_keywords.keys(), result) if count > 0)
                print("Single category identified:", category_with_match)
                print(f"result - {result}")
                return category_with_match

            # if non_zero_count > 1:  # Cover both multiple categories and no matches
            else:
                print("It seems your query falls under multiple categories. Please rephrase your statement.")
                print(f"result - {result}")
                multi_category = "multiple"
                return multi_category
            
            # else:
            #     print("It seems out of scope")
            #     print(f"result - {result}")
            #     oos_category = "out of scope"
            #     return oos_category

            # if len(found_keywords) > 1:
            #     print("It seems your query falls under multiple categories. Please rephrase your statement.")
            #     print(f"inside multiple cateory - {[len(words) for words in found_keywords.values()]}")
            #     # Return a list containing the counts for each category
            #     return [len(words) for words in found_keywords.values()]

            # else:
            #     # Return the words for the single category
            #     print(f"inside single cateory - {found_keywords[next(iter(found_keywords))]}")
            #     return found_keywords[next(iter(found_keywords))]

#  -----------------

        # for word in cleaned_words:
        #     # print(word)
        #     if supplier_regex.search(word):
        #         found_keywords.append(word)
        #     elif order_regex.search(word):
        #         found_keywords.append(word)
        #     elif inventory_regex.search(word):
        #         found_keywords.append(word)
        #     elif pricing_regex.search(word):
        #         found_keywords.append(word)
 

        # if found_keywords:
        #     print(found_keywords)
        #     if len(set(found_keywords)) > 1:
        #         print("It seems your query falls under multiple categories. Please rephrase your statement.")
        #         print(f"Words found in category1: {set(found_keywords)}")
        #         return [len(set(found_keywords))]

        #     else:
        #         print(f"Words found in category2: {found_keywords[0]}")
        #         return found_keywords[0]

        # if found_keywords:
        #     print("Words found:")
        #     for word in found_keywords:
        #         print(f"found1 {word}")
        #         return word

        # else:
        #     cleaned_words = self.remove_punctuation(word_list)
        #     #if the words has more than two syllable, split and check for the intent
        #     for words in cleaned_words:
        #         words_array = words.split()
        #         for word in words_array:
        #             if word  in supplier_keywords_lower:
        #                 found_keywords.append("supplier")
        #             elif word  in order_keyword_lower:
        #                 found_keywords.append("Order")
        #             elif word  in inventory_keywords_lower:
        #                 found_keywords.append("inventory")
        #             elif word  in pricing_keywords_lower:
        #                 found_keywords.append("pricing")

        #         if found_keywords:
        #             print("Words found:")
        #             for word in found_keywords:
        #                 print(word)
        #                 return word
        # if found_keywords:
        #     if len(set(found_keywords)) > 1:
        #         print("It seems your query falls under multiple categories. Please rephrase your statement.")
        #         return [len(set(found_keywords))]
        #     else:
        #         print(f"Words found in category3: {found_keywords[0]}")
        #         return found_keywords[0]

#-------------------------------------------------------
    def correct_spelling(self,sentence):
        spell = SpellChecker()
        words = sentence.split()
        corrected_words = [spell.correction(word) for word in words]
        corrected_sentence = ' '.join(corrected_words)
        return corrected_sentence
    

    def translate_and_print_language(self, user_input):

        translator = Translator()

        translation = translator.translate(user_input, dest='en')

        full_source_language_name = LANGUAGES.get(translation.src)

        print(f"source language key: {translation.src}")
        print(f"Source Language full name: {full_source_language_name}")
        print(f"Translated Text: {translation.text}")
        print("------------------------")
        return full_source_language_name,translation.text
    
    def langToEng(self, keyword, language):
        dict_l = {'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'he': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'or': 'odia', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu'}
        # print(f"dict_l---->{dict_l}")
        translator = Translator()
        # Detect the source language
        # detection = translator.detect(text)
        # src_lang = detection.lang
        # print(f"Detected source language: {dict_l[src_lang]}")
        print(f"lang:{language}")
        self.language = language.lower()
        print(self.language)
        #taking the key for the value - from dictionaty
        # print("One line Code Key value: ", list(dict_l.keys())
        #   [list(dict_l.values()).index(language)])
        key_of_lang=list(dict_l.keys())[list(dict_l.values()).index(self.language)]
 
        # Translating the text to English
        main_out = translator.translate(keyword, dest='en', src=key_of_lang)
        text_val = main_out.text
        user_lang = key_of_lang
        # Print the results
        print(f"Source language: {language}")
        print(f"English translation: {text_val}")
        # Update the global class variable
        allFunc.key_of_lang = user_lang
        return text_val, user_lang


   
    def Eng_to_user_language(self, response, lang):
        if response is None:
            return None
        # dict_l = googletrans.LANGUAGES
        translator = Translator()
        # key_of_lang=list(dict_l.keys())[list(dict_l.values()).index(language)]
        print(f"response to Eng_to_user_language {response}")
        if lang is None:
            lang = 'en'
        # Translating the text to English
        main_out = translator.translate(response, dest=lang, src='en')
        text_val = main_out.text

        return text_val
# #          # Create a translator object
#  # Create a translator object
#         translator = Translator()

#         # Split the response into lines
#         response_lines = response.split('\n')
#         print("1")
#         print(response_lines)

#         # Translate and print each line
#         translated_lines = []
#         for line in response_lines:
#             # Split each line into key and value
#             key, value = line.split(': ', 1) if ': ' in line else (line, '')
#             print("2")

#             print(key)
#             print("3")

#             print(value)

#             # Translate only the value part
#             # translated_value = translator.translate(value, dest=lang, src='en').text
#             translated_value = translator.translate(key, dest=lang, src='en').text

#             print("4")

#             print(translated_value)

#             # Join the translated key and translated value
#             translated_line = f"{translated_value}: {value}"
#             translated_lines.append(translated_line)

#         # Join the translated lines
#         translated_response = '\n'.join(translated_lines)
#         print("5")

#         print(translated_response)

#         return translated_response
    
        # translator = Translator()

        # # Detect the language using langid
        # lang, _ = langid.classify(user_input)

        # # Translate the text to English
        # translation = translator.translate(user_input, dest='en')

        # # Get the full language name
        # full_source_language_name = LANGUAGES.get(lang)

        # print(f"Source Language: {full_source_language_name}")
        # print(f"Translated Text: {translation.text}")

        # return translation

    def check_plural(self,word):
        p = inflect.engine()
        plural_form = p.plural(word)
        return plural_form

    def download_as_file(self, output_dict):
        # Sample data
        # item_data = [
        #     {"item_no": "100190308", "location": "102", "location_type": "S", "price": "1025"},
        #     {"item_no": "100185305", "location": "105", "location_type": "S", "price": "19266.69"},
        #     {"item_no": "100035000", "location": "607", "location_type": "S", "price": "275.25"}
        # ]
        # Create a DataFrame from the list of dictionaries
            df = pd.DataFrame(output_dict)

            # Save the DataFrame to an Excel file
            filename = "item_prices_u1.xlsx"
            # filename = "/app/excel_files/item_prices_u1.xlsx"

            df.to_excel(filename, index=False)

            # Move the file to the Downloads directory (similar to previous code)
            file_path = os.path.join(os.getcwd(), filename)
            downloads_path = os.path.expanduser("~\\Downloads")
            # downloads_path = "/app/excel_files"
            new_file_path = os.path.join(downloads_path, filename)
            shutil.move(file_path, new_file_path)

            # Get the file URL for sending to the user
            file_url = f"file://{new_file_path}"
            return file_url
        #     Get the user's home directory (common folder for both Linux and Windows)
        # df = pd.DataFrame(output_dict)

        # # Save the DataFrame to an Excel file
        # filename = "item_prices_u1.xlsx"
        # df.to_excel(filename, index=False)

        # # Get the user's home directory (common folder for both Linux and Windows)
        # home_directory = os.path.expanduser("~")

        # # Define the target directory (Downloads on Windows, or a common folder on Linux)
        # if os.name == "nt":  # 'nt' stands for Windows OS
        #     target_directory = os.path.join(home_directory, "Downloads")
        # else:
        #     # For Linux, you can specify any common folder where you have write access
        #     target_directory = os.path.join(home_directory, "my_common_folder")

        # # Move the file to the target directory
        # file_path = os.path.join(os.getcwd(), filename)
        # new_file_path = os.path.join(target_directory, filename)
        # shutil.move(file_path, new_file_path)

        # # Get the file URL for sending to the user
        # file_url = f"file://{new_file_path}"

            # return file_url  # Return the file URL for further processing
            # return f"[Click here to download the file]({file_url})"
        # return file_url
    


    def format_table_no_borders(table_data, table_headers):
        output = f"{' | '.join(table_headers)}\n"
        for row in table_data:
            row_data = [str(cell) if cell is not None else "" for cell in row]
            output += f"{' | '.join(row_data)}\n"
        return output

    # # Sample data for the table
    # table_headers = ["Item", "Location", "Location Type", "Qty Ordered", "Qty Received"]
    # table_data = [
    #     {"Item": "100040002", "Location": "1075", "Location Type": "S", "Qty Ordered": "10", "Qty Received": "10"},
    #     {"Item": "100040003", "Location": "1075", "Location Type": "S", "Qty Ordered": "10", "Qty Received": "10"},
    #     {"Item": "100040004", "Location": "1075", "Location Type": "S", "Qty Ordered": "10", "Qty Received": "10"},
    #     {"Item": "100040005", "Location": "1075", "Location Type": "S", "Qty Ordered": "10", "Qty Received": "10"},
    # ]
