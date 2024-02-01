import requests
from use_cases.FileDownloader.ExcelFileDownloader import ExcelFileDownloader
class ItemDetails:
    @staticmethod
    def get_item_details(self, item_no, access_token):
        self.item_no = item_no
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
                'ItemGrandparent ': itemGrandparent,
                'ItemParent ': itemParent,
                'Item ': item,
                'ItemDesc ': itemDesc,
                'Status ': status,
                'ItemLevel ': itemLevel,
                'TranLevel ': tranLevel

            }
            if item_data:
                 # Call the download_excel function from the FileDownloader class
                file_url = ExcelFileDownloader.download_excelfile_in_server([item_data], "item_info.xlsx")

                return item_details, file_url
            
        else:
            print("Failed to get API response. Status Code:", response.status_code)
            return None, None