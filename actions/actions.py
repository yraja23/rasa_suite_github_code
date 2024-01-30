import re,requests
import re
import pandas as pd
import shutil
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, ValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet,FollowupAction, UserUttered, ActionExecuted
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.types import DomainDict
import os
import yaml
from .trydb import jsonConversion, allFunc
# from .geminipro import jsonConversion, allFunc
import ast
# import nltk
# nltk.download('punkt')
import json
from typing import Text, Any, Dict
# from nltk.corpus import wordnet
from .geminipro import Geminipro
# from rasa.shared.nlu.training_data.readers.markdown_reader import MarkdownReader
# # from bardapi import bard
# # import bardapi.core
# import logging
class CustomAction(Action):
    def name(self) -> Text:
        return "custom_action"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve information from the conversation
        # user_value = tracker.latest_message("text")
        user_value = tracker.latest_message['text']
        #incase if the sentence is stored completely, extract the number
        number = re.search(r'\d+', user_value).group()
        # Set the value of a slot using the reusable function
        return [SlotSet("item", number),SlotSet("item_value", number)]
    
class CustomAction1(Action):
    def name(self) -> Text:
        return "custom_action_for_loc"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve information from the conversation
        # user_value = tracker.latest_message("text")
        item_value=tracker.get_slot("item_value")
        print(item_value)
        user_value = tracker.latest_message['text']
        print(user_value)
        #incase if the sentence is stored completely, extract the number
        number = re.search(r'\d+', user_value).group()
        print()
        # Set the value of a slot using the reusable function
        return [SlotSet("loc", number), SlotSet("item", item_value)]
    
class ItemDetailsOauthApi(Action):
    def name(self) -> Text:
        return "action_all_item_prices"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:        
        filename = "encrypted_client_details.ini"
        out = jsonConversion()
        access_token = out.generate_token(filename)

        if access_token:
            allItemPrices, file_url = out.get_api_response_usecase1(access_token)
            # out=str(allItemPrices)
            # print(out)
            # Send the JSON data as a message
            if isinstance(allItemPrices, list):
                for item_data in allItemPrices:
                    message = ""
                    for key, value in item_data.items():
                        message += f"{key}: {value}\n"
                    # dispatcher.utter_message(text=message)
            # else:
            #     dispatcher.utter_message(text=allItemPrices)
                # allItemPrices = [allItemPrices]  

            lang = allFunc.key_of_lang
            print("Class variable:", allFunc.key_of_lang)
            if lang != 'en':
                response_user_lang = allFunc.Eng_to_user_language(self, allItemPrices, lang)
                if allItemPrices is None and response_user_lang is None:
                    dispatcher.utter_message("Looks like there is no data present for the mentioned order or the order does not exist. You can try checking for different values.")            
                else:
                    dispatcher.utter_message(text=allItemPrices)
                    dispatcher.utter_message(text=response_user_lang)
            else:
                dispatcher.utter_message(text=allItemPrices)  
#               
            if file_url:
                dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")
        return[]

class Itemdetails(Action):
    def name(self)-> Text:
        return "action_get_pricedetail"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # #instead of custom action, slot is set here and called as functions
        # self.slot_set_item_uc2(tracker)
        # self.slot_set_loc_uc2(tracker)
        item =tracker.get_slot('item')
        loc = tracker.get_slot('loc')
       
        filename = "encrypted_client_details.ini"
        out = jsonConversion()
        access_token= out.generate_token(filename)
        if access_token:
            get_price_detail, file_url =out.get_api_response(access_token,item,loc)    
            if isinstance(get_price_detail, list):
                lang = allFunc.key_of_lang
                print("Class variable:", allFunc.key_of_lang)
                for item_data in get_price_detail:
                    message = ""
                    for key, value in item_data.items():
                        message += f"{key}: {value}\n"

            lang = allFunc.key_of_lang
            print("Class variable:", allFunc.key_of_lang)
            if lang != 'en' and lang is not None:
                response_user_lang = allFunc.Eng_to_user_language(self, get_price_detail, lang)
                if get_price_detail is None and response_user_lang is None:
                    dispatcher.utter_message("Looks like there is no data present for the mentioned order or the order does not exist. You can try checking for different values.")            
                else:
                    dispatcher.utter_message(text=get_price_detail)
                    dispatcher.utter_message(text=response_user_lang)
            else:
                dispatcher.utter_message(text=get_price_detail)  
               
            if file_url:
                dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")
        return [SlotSet('item', None), SlotSet('loc', None), SlotSet('item_prev', item), SlotSet('item_value_prev', loc), SlotSet('uc2_output', get_price_detail)]
   
        #     else:
        #         # Wrap the error message in a list
        #         dispatcher.utter_message(text=get_price_detail)
        #         get_price_detail = [get_price_detail]  

        #     if lang != 'en':
        #         dispatcher.utter_message(text=translated_message)
        #         dispatcher.utter_message(text=get_price_detail)
        #     else:
        #         dispatcher.utter_message(text=get_price_detail)

        #     if file_url:
        #         dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")
        # return [SlotSet('item', None), SlotSet('loc', None), SlotSet('item_prev', item), SlotSet('item_value_prev', loc), SlotSet('uc2_output', get_price_detail)]
class GetPriceatAllLocation(Action):
    def name(self)-> Text:
        return "action_getPrice_at_All_Location"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        item_loc = tracker.latest_message['text']
        # item= tracker.get_slot("item")
        # print(item_loc+item)
        filename = "encrypted_client_details.ini"
        out = jsonConversion()
        access_token = out.generate_token(filename)
        if access_token:
            allItemPrices, file_url = out.get_api_response_usecase3(access_token,item_loc)
            print(f"all item {allItemPrices}")
            if isinstance(allItemPrices, list):
                lang = allFunc.key_of_lang
                print("Class variable:", allFunc.key_of_lang)
                for item_data in allItemPrices:
                    message = ""
                    for key, value in item_data.items():
                        message += f"{key}: {value}\n"

            lang = allFunc.key_of_lang
            print("Class variable:", allFunc.key_of_lang)
            if lang != 'en' and lang is not None:
                response_user_lang = allFunc.Eng_to_user_language(self, allItemPrices, lang)
                if allItemPrices is None and response_user_lang is None:
                    dispatcher.utter_message("Looks like there is no data present for the mentioned order or the order does not exist. You can try checking for different values.")            
                else:
                    dispatcher.utter_message(text=allItemPrices)
                    dispatcher.utter_message(text=response_user_lang)
            else:
                dispatcher.utter_message(text=allItemPrices)  
               
            if file_url:
                dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")   
        return[SlotSet('item_value', item_loc),SlotSet('item_loc', item_loc), SlotSet('uc3_output', allItemPrices)]

# class GetPriceatAllLocation(Action):
#     def name(self)-> Text:
#         return "action_getPrice_at_All_Location"
    
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         item_loc = tracker.latest_message['text']
#         item= tracker.get_slot("item")
#         filename = "encrypted_client_details.ini"
#         out = jsonConversion()
#         access_token = out.generate_token(filename)
#         if access_token:
#             allItemPrices, file_url = out.get_api_response_usecase3(access_token,item_loc)
#             if isinstance(allItemPrices, list):
#                 lang = allFunc.key_of_lang
#                 print("Class variable:", allFunc.key_of_lang)
#                 for item_data in allItemPrices:
#                     message = ""
#                     for key, value in item_data.items():
#                         message += f"{key}: {value}\n"

#             lang = allFunc.key_of_lang
#             print("Class variable:", allFunc.key_of_lang)
#             if lang != 'en':
#                 response_user_lang = allFunc.Eng_to_user_language(self, allItemPrices, lang)
#                 if allItemPrices is None and response_user_lang is None:
#                     dispatcher.utter_message("Looks like there is no data present for the mentioned order or the order does not exist. You can try checking for different values.")            
#                 else:
#                     dispatcher.utter_message(text=allItemPrices)
#                     dispatcher.utter_message(text=response_user_lang)
#             else:
#                 dispatcher.utter_message(text=allItemPrices)  
           
#             if file_url:
#                 dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")

#             return[SlotSet('item_value', item_loc),SlotSet('item_loc', item_loc), SlotSet('uc3_output', allItemPrices)]


class CustomActionUtterRepeat(Action):
    def name(self) -> Text:
        return "action_utter_display_prev_item"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        item_prev = tracker.get_slot('item_prev')
        item_value_prev = tracker.get_slot('item_value_prev')
        specific_output = tracker.get_slot('uc2_output')
        print(f"specific output {specific_output}")
        
        if specific_output == None and item_prev:
            dispatcher.utter_message(f"Earlier you have checked details for the item {item_prev} at the location {item_value_prev} and looks like there was no data present or there could have been an error in the data that was entered..")
            dispatcher.utter_message("If you want to check for a different item, or to check for different locations,")
        elif item_prev and item_value_prev or specific_output:
            dispatcher.utter_message(f"Earlier you have checked details for the item {item_prev} at the location {item_value_prev}.\n And the details related to your previous search was \n{specific_output}")
            dispatcher.utter_message("If you want to check for a different item, or to check for different locations,")
        else:
            print("the values are none. story continues..")
        return []
    
class CustomActionUtterRepeatUc3(Action):
    def name(self) -> Text:
        return "action_utter_display_prev_item_uc3"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        item_value = tracker.get_slot('item_loc')
        uc3_output = tracker.get_slot('uc3_output')
        #if condition for the 3rd usecase - item at all lcoation
        if item_value:
            dispatcher.utter_message(f"Earlier you have checked details for the item {item_value}.\n Here is the price details of the item {item_value} at all location.\n {uc3_output}")
            dispatcher.utter_message("If you want to check for a different item's detail, feel free to, ")
        else:
            print("the values are none. story continues..")
        return []   

class SupplierAction(Action):
    def name(self) -> Text:
        return "action_supplier_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # supplier_no = tracker.latest_message['text']

        supplier_no = tracker.get_slot('numeric_values')
        # dispatcher.utter_message("Accessing...")
        
        if not supplier_no or not supplier_no.isnumeric():
            dispatcher.utter_message("Please enter a valid numeric value for the supplier.")
            return []
        filename = "encrypted_client_details.ini"
        out = jsonConversion()
        access_token = out.generate_token(filename)
        # print(access_token)
        if access_token:
            supplier_details, file_url = out.supplier_details(supplier_no,access_token)
            # print(supplier_details)
            # print(file_url)
            if isinstance(supplier_details, list):
                # print("inside if")
                for item_data in supplier_details:
                    message = ""
                    for key, value in item_data.items():
                        message += f"{key}: {value}\n"
                    dispatcher.utter_message(text=message)
            
            lang = allFunc.key_of_lang
            print("Class variable:", allFunc.key_of_lang)
            if lang != 'en':
                response_user_lang = allFunc.Eng_to_user_language(self, supplier_details, lang)
                if supplier_details is None and response_user_lang is None:
                    dispatcher.utter_message("Looks like there is no data present for the mentioned supplier or the supplier does not exist. You can try checking for different values.")
                    return [SlotSet('supplier_value',supplier_no),SlotSet('supplier_output',supplier_details),SlotSet('numeric_values',None)]  
                else:
                    dispatcher.utter_message(text=supplier_details)
                    dispatcher.utter_message(text=response_user_lang)
            else:
                dispatcher.utter_message(text=supplier_details) 

            if file_url:
                dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")

        return [SlotSet('supplier_value',supplier_no),SlotSet('supplier_output',supplier_details),SlotSet('numeric_values',None)]  

  
            # dispatcher.utter_message("Accessing...")
            # out=str(allItemPrices)
            # if allItemPrices == None:
            #     # print("inside action else part")
            #     dispatcher.utter_message("Looks like, the item is not present in the mentioned location.\n you can try checking if the entered values are correct or try searching for different values.")
            # dispatcher.utter_message(text=allItemPrices)
            #error message is also returned from the file. So  both are pprinted through the if statement.
 
       
class displayPrevForSupplierUsecase(Action):
    def name(self) -> Text:
        return "action_prevData_for_supplier"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        prev_supplierno = tracker.get_slot('supplier_no')
        output_supplier=tracker.get_slot('supplier_details')

        if output_supplier == None and prev_supplierno:
            dispatcher.utter_message(f"Earlier you have checked the supplier details for the supplier {prev_supplierno} and looks like there was no data present or there could have been an error in the data that was entered..")
        elif prev_supplierno and output_supplier:
            dispatcher.utter_message(f"Earlier you have checked the supplier details for the supplier {prev_supplierno}.\n And the details related to your previous search was \n{output_supplier}")
            dispatcher.utter_message("If you want to check for a different item, or to check for different locations,")
        else:
            print("the values are none. story continues..")

class InventoryAction(Action):
    def name(self) -> Text:
        return "action_inventory_details_for_store"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #button value is captured using inernal function and stored in the slot - button is used to reduce the number of actions
        inv_locType="S"
        inv_loc = tracker.get_slot("inv_loc")
        filename = "encrypted_client_details.ini"
        out = jsonConversion()
        access_token = out.generate_token(filename)

        if access_token:
            inventoryDetails, file_url = out.inventory_details_for_store(inv_loc,inv_locType,access_token)
            if isinstance(inventoryDetails, list):
                for item_data in inventoryDetails:
                    message = ""
                    for key, value in item_data.items():
                        message += f"{key}: {value}\n"
                    # dispatcher.utter_message(text=message)

            lang = allFunc.key_of_lang
            print("Class variable:", allFunc.key_of_lang)
            translated_message = allFunc.Eng_to_user_language(self, inventoryDetails, lang)

            if lang is None:
                lang = 'en'
            if lang != 'en':
                dispatcher.utter_message(text=inventoryDetails)
                dispatcher.utter_message(text=translated_message)
            else:
                dispatcher.utter_message(text=inventoryDetails)

            if file_url:
                dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")
                return [SlotSet('inv_loc',inv_loc),SlotSet('inv_locType',inv_locType),SlotSet('inventory_output',inventoryDetails)]    
            
        return [SlotSet('inv_loc',inv_loc),SlotSet('inv_locType',inv_locType),SlotSet('inventory_output',inventoryDetails)]    


        #     inventoryDetails, file_url = out.inventory_details_for_store(inv_loc,inv_locType,access_token)

       
        #     if isinstance(inventoryDetails, list):
        #         lang = allFunc.key_of_lang
        #         print("Class variable:", allFunc.key_of_lang)
        #         for item_data in inventoryDetails:
        #             message = ""
        #             for key, value in item_data.items():
        #                 message += f"{key}: {value}\n"
        #             # translated_message = allFunc.Eng_to_user_language(self, inventoryDetails, lang)

        #     if inventoryDetails is None:
        #         dispatcher.utter_message("Looks like there is no data for the given location and location type or the number doesn't exist. You can try checking for different values.")
        #         return [SlotSet('inv_loc',inv_loc),SlotSet('inv_locType',inv_locType),SlotSet('inventory_output',inventoryDetails)]
    

        #     lang = allFunc.key_of_lang
        #     print("Class variable:", allFunc.key_of_lang)
        #     if lang is None:
        #         lang = 'en'
        #     if lang != 'en':
        #         dispatcher.utter_message(text=translated_message)
        #         dispatcher.utter_message(text=inventoryDetails)
        #     else:
        #         dispatcher.utter_message(text=inventoryDetails)

        #     if file_url:
        #         dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")

        #     # if file_url:
        #     #     dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")
        #     #     return [SlotSet('inv_loc',inv_loc),SlotSet('inv_locType',inv_locType),SlotSet('inventory_output',inventoryDetails)]    
            
        #     # if inventoryDetails is None:
        #     #     dispatcher.utter_message("Looks like there is no data present for the given location and location type or the number doesn't exist. You can try checking for different values.")
        #     # dispatcher.utter_message(text=inventoryDetails)
        # return [SlotSet('inv_loc',inv_loc),SlotSet('inv_locType',inv_locType),SlotSet('inventory_output',inventoryDetails)]    

class InventoryActionWH(Action):
    def name(self) -> Text:
        return "action_inventory_details_for_wh"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #button value is captured using inernal function and stored in the slot - button is used to reduce the number of actions
        inv_locType="W"
        inv_loc = tracker.get_slot("inv_loc")
        filename = "encrypted_client_details.ini"
        out = jsonConversion()
        access_token = out.generate_token(filename)
        # print(access_token)

        if access_token:
            inventoryDetails , file_url = out.inventory_details_for_wh(inv_loc,inv_locType,access_token)
            if isinstance(inventoryDetails, list):
                for item_data in inventoryDetails:
                    message = ""
                    for key, value in item_data.items():
                        message += f"{key}: {value}\n"
                    # dispatcher.utter_message(text=message)

            lang = allFunc.key_of_lang
            print("Class variable:", allFunc.key_of_lang)
            translated_message = allFunc.Eng_to_user_language(self, inventoryDetails, lang)

            if lang is None:
                lang = 'en'
            if lang != 'en':
                dispatcher.utter_message(text=inventoryDetails)
                dispatcher.utter_message(text=translated_message)
            else:
                dispatcher.utter_message(text=inventoryDetails)

            if file_url:
                dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")
                return [SlotSet('inv_loc',inv_loc),SlotSet('inv_locType',inv_locType),SlotSet('inventory_output',inventoryDetails)]    
            
        return [SlotSet('inv_loc',inv_loc),SlotSet('inv_locType',inv_locType),SlotSet('inventory_output',inventoryDetails)]    

        #     inventoryDetails , file_url = out.inventory_details_for_wh(inv_loc,inv_locType,access_token)
        #     if isinstance(inventoryDetails, list):
        #         lang = allFunc.key_of_lang
        #         print("Class variable:", allFunc.key_of_lang)
        #         for item_data in inventoryDetails:
        #             message = ""
        #             for key, value in item_data.items():
        #                 message += f"{key}: {value}\n"
        #             translated_message = allFunc.Eng_to_user_language(self, message, lang)


        #     if inventoryDetails is None and translated_message is None:
        #         dispatcher.utter_message("Looks like there is no data for the given location and location type or the number doesn't exist. You can try checking for different values.")
        #         return [SlotSet('inv_loc',inv_loc),SlotSet('inv_locType',inv_locType),SlotSet('inventory_output',inventoryDetails)]

        #     lang = allFunc.key_of_lang
        #     print("Class variable:", allFunc.key_of_lang)
        #     if lang != 'en':
        #         dispatcher.utter_message(text=translated_message)
        #         dispatcher.utter_message(text=inventoryDetails)
        #     else:
        #         dispatcher.utter_message(text=inventoryDetails)

        #     if file_url:
        #         dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")

        # return [SlotSet('inv_loc',inv_loc),SlotSet('inv_locType',inv_locType),SlotSet('inventory_output',inventoryDetails)]    

        #     # dispatcher.utter_message("Accessing...")
        #     if isinstance(inventoryDetails, list):
        #         for item_data in inventoryDetails:
        #             message = ""
        #             for key, value in item_data.items():
        #                 message += f"{key}: {value}\n"
        #             dispatcher.utter_message(text=message)


        #     lang = allFunc.key_of_lang
        #     print("Class variable:", allFunc.key_of_lang)
        #     if lang != 'en':
        #         response_user_lang = allFunc.Eng_to_user_language(self, inventoryDetails, lang)
        #         if inventoryDetails is None and response_user_lang is None:
        #             dispatcher.utter_message("Looks like there is no data for the given location and location type or the number doesn't exist. You can try checking for different values.")
        #             return [SlotSet('inv_loc',inv_loc),SlotSet('inv_locType',inv_locType),SlotSet('inventory_output',inventoryDetails)]
        #         else:
        #             print(f"response_user_lang {response_user_lang}")
        #             dispatcher.utter_message(text=response_user_lang)
        #     else:
        #         dispatcher.utter_message(text=inventoryDetails)

        #     if file_url:
        #         dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")

        # return [SlotSet('inv_loc',inv_loc),SlotSet('inv_locType',inv_locType),SlotSet('inventory_output',inventoryDetails)]    

class displayPrevForInvUsecase(Action):
    def name(self) -> Text:
        return "action_prevData_for_inv"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prev_inv = tracker.get_slot('item_for_inventory')
        output_inv=tracker.get_slot('inventoryDetails')

        if output_inv == None and prev_inv:
            dispatcher.utter_message(f"Earlier you have checked the inventory details for the location {prev_inv} and looks like there was no data present or there could have been an error in the data that was entered..")
        elif prev_inv and output_inv:
            dispatcher.utter_message(f"Earlier you have checked the inventory details for the location {prev_inv}.\n And the details related to your previous search was \n{output_inv}")
            dispatcher.utter_message("If you want to check for a different item, or to check for different locations,")
        else:
            print("the values are none. story continues..")

class InventoryLocationCapture(Action):
    def name(self) -> Text:
        return "action_inventory_store_loc"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # inv_loc = tracker.get_slot('inv_loc')
        # inv_loc_type = tracker.get_slot('inv_locType')
        user_value = tracker.latest_message['text']
        return[SlotSet('inv_loc',user_value)]
  
class OrderAction(Action):
    def name(self) -> Text:
        return "action_order_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # order_no = tracker.latest_message['text']
        order_no = tracker.get_slot('numeric_values')
        # dispatcher.utter_message("Accessing...")
        filename = "encrypted_client_details.ini"
        out = jsonConversion()
        access_token = out.generate_token(filename)
        if access_token:
            orderDetails, file_url = out.order_details(order_no,access_token)
            print(orderDetails)
            print(file_url)

            if isinstance(orderDetails, list):
                for item_data in orderDetails:
                    message = ""
                    for key, value in item_data.items():
                        message += f"{key}: {value}\n"
                    # dispatcher.utter_message(text=message)

           
            # if orderDetails is None:
            #     # print("inside none")
            #     dispatcher.utter_message("Looks like there is no data present for the mentioned order or the order does not exist. You can try checking for different values.")

            lang = allFunc.key_of_lang
            print("Class variable:", allFunc.key_of_lang)
            if lang != 'en' or lang is None:
                response_user_lang = allFunc.Eng_to_user_language(self, orderDetails, lang)
                if orderDetails is None and response_user_lang is None:
                    dispatcher.utter_message("Looks like there is no data present for the mentioned order or the order does not exist. You can try checking for different values.")
                    return [SlotSet('order_value',order_no),SlotSet('order_output',orderDetails)] 
                else:
                    # print(f"response_user_lang {response_user_lang}")
                    dispatcher.utter_message(text=orderDetails) 
                    dispatcher.utter_message(text=response_user_lang) 

            else:
                dispatcher.utter_message(text=orderDetails) 

            if file_url:
                dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")
                return [SlotSet('order_value',order_no),SlotSet('order_output',orderDetails)]  

        return [SlotSet('order_value',order_no),SlotSet('order_output',orderDetails)] 
    
# -------------------------------------------------------------------------------------
 
class ItemAction(Action):
    def name(self) -> Text:
        return "action_item_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # order_no = tracker.latest_message['text']
        item_no = tracker.get_slot('numeric_values')
        # dispatcher.utter_message("Accessing...")
        filename = "encrypted_client_details.ini"
        out = jsonConversion()
        access_token = out.generate_token(filename)
        if access_token:
            itemDetails, file_url = out.item_details(item_no,access_token)  
            # print(itemDetails)
            # print(file_url)
            # dispatcher.utter_message(text=itemDetails)

            # if isinstance(itemDetails, list):
            #     for item_data in itemDetails:
            #         message = ""
            #         for key, value in item_data.items():
            #             message += f"{key}: {value}\n"
            #     dispatcher.utter_message(text=message)



            # if itemDetails is None:
            #     dispatcher.utter_message("Looks like there is no data present for the mentioned order or the order does not exist. You can try checking for different values.")
            #     return [SlotSet('supplier_value',item_no),SlotSet('supplier_output',itemDetails),SlotSet('numeric_values',None)]  
#
            lang = allFunc.key_of_lang
            print("Class variable:", allFunc.key_of_lang)
            if lang != 'en':
                response_user_lang = allFunc.Eng_to_user_language(self, itemDetails, lang)
                if itemDetails is None and response_user_lang is None:
                    dispatcher.utter_message("Looks like there is no data present for the mentioned order or the order does not exist. You can try checking for different values.")
                    return [SlotSet('supplier_value',item_no),SlotSet('supplier_output',itemDetails),SlotSet('numeric_values',None)]  
            
                else:
                    dispatcher.utter_message(text=itemDetails)
                    dispatcher.utter_message(text=response_user_lang)
            else:
                dispatcher.utter_message(text=itemDetails)  
#               
            if file_url:
                dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")
                return [SlotSet('item_value',item_no)]  
        return [SlotSet('supplier_value',item_no),SlotSet('supplier_output',itemDetails),SlotSet('numeric_values',None)]  
    
    # -------------------------------------------------------------------------------------
class displayPrevForOrderUsecase(Action):
    def name(self) -> Text:
        return "action_prevData_for_order"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        prev_orderno = tracker.get_slot('order_no')
        output_order=tracker.get_slot('orderDetails')

        # #getting the intent that is being chosen, and displaying the message based on it
        # intent_name = tracker.latest_message['intent'].get('name')

        if output_order == None and prev_orderno:
            dispatcher.utter_message(f"Earlier you have checked the supplier details for the number {prev_orderno} and looks like there was no data present or there could have been an error in the data that was entered..")
        elif prev_orderno and output_order:
            dispatcher.utter_message(f"Earlier you have checked the supplier details for the number {prev_orderno}.\n And the details related to your previous search was \n{output_order}")
            dispatcher.utter_message("If you want to check for a different item, or to check for different locations,")
        else:
            print("the values are none. story continues..")


class SupplierWithNumberAction(Action):
    def name(self) -> Text:
        return "action_supplier_with_number_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # user_message = tracker.latest_message['text']
        sup1=tracker.get_slot('supplier_with_number')
        print("supplier_detail_from_slot",sup1)
        # dispatcher.utter_message(user_message)
        # dispatcher.utter_message(supplier_no)
        filename = "encrypted_client_details.ini"
        out = jsonConversion()
        access_token = out.generate_token(filename)
        # print(access_token)
        if access_token:
            supplier_details, file_url = out.supplier_details(sup1,access_token)
            if isinstance(supplier_details, list):
                print("inside if")
                for item_data in supplier_details:
                    message = ""
                    for key, value in item_data.items():
                        message += f"{key}: {value}\n"
                    dispatcher.utter_message(text=message)
            
            if supplier_details is None:
                print("inside none")
                dispatcher.utter_message("Looks like there is no data present for the mentioned supplier or the supplier does not exist. You can try checking for different values.")
            dispatcher.utter_message(text=supplier_details)      

            if file_url:
                dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")


        return [SlotSet('supplier_value',sup1),SlotSet('supplier_output',supplier_details),SlotSet('numeric_values',None)]  


class OrderWithNumberAction(Action):
    def name(self) -> Text:
        return "action_order_with_number_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_no=tracker.get_slot('order_with_number')
        print("order_detail_from_slot",order_no)

        filename = "encrypted_client_details.ini"
        out = jsonConversion()
        access_token = out.generate_token(filename)
        if access_token:
            orderDetails, file_url = out.order_details(order_no,access_token)
            print(orderDetails)
            print(file_url)

            if isinstance(orderDetails, list):
                for item_data in orderDetails:
                    message = ""
                    for key, value in item_data.items():
                        message += f"{key}: {value}\n"
                    dispatcher.utter_message(text=message)

            if file_url:
                dispatcher.utter_message(text=f"[Click here to download the file]({file_url})", parse_mode="markdown")
                return [SlotSet('order_value',order_no),SlotSet('order_output',orderDetails)]  

            if orderDetails == None:
                # print("inside none")
                dispatcher.utter_message("Looks like there is no data present for the mentioned order or the order does not exist. You can try checking for different values.")
            dispatcher.utter_message(text=orderDetails) 


        return [SlotSet('order_value',order_no),SlotSet('order_output',orderDetails),SlotSet('numeric_values',None)] 

#-------------------------------------------STAGE 2 ------------------------------------------------------------------------------  
#user_input_question entity is not used, as entity was only used to check only the condition.
#taking the latest message from the user only will work fine, if the functions are redirected in this action.
#(redirection step is added - but since it didn't work, adding the steps from the two functios again directly here)
#THIS ACTION IS TRIGGERED WHENEVER THE USER ENTERS A STATEMENT - checks if it is retail specific or non retail specific and works accordingly
class CheckKeywordAction(Action):

    def name(self) -> Text:
        return "check_value_in_intent"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Get the user input from the tracker
        keyword=tracker.latest_message.get("text")
        print("------------------------------------------")
        print(f"before: {keyword}")

        # Identify the language of the user input using Geminipro 
        gemini_instance = Geminipro()
        user_input = f"Identify the language of the phrase '{keyword}'. Simply provide the language name."
        print(f"befor bard call user_input {user_input}")
        lang = gemini_instance.send_message_and_get_response(keyword) 
        print("Model's response:", lang)

        # Translate the user input to English
        object=allFunc()
        translation,key_of_lang = object.langToEng(keyword, lang)
        print(f"translation {translation}")
        print(f"lang_key {key_of_lang}")

        check_user_input_isRetail = f"Is the phrase '{translation}' related to the retail domain? Please respond with a simple 'Yes' or 'No' without providing an explanation."
        object=allFunc()
        response = object.palmApi(check_user_input_isRetail)
        print(f"Printing the Palm response for the user input to determine if it belongs to the retail domain: {response}")
        if response.lower() == 'no' :
            error_text = "I apologize, but it looks like the information that you are trying to get is not retail specific.\n\
                        You can ask me anything related the domain, I will do my best to help you in any way that I can."      
            dispatcher.utter_message(text=error_text)
            return [FollowupAction("utter_price_details")]  
        else:

            response1= gemini_instance.extract_nouns(translation)
            print("after noun call")
            print(f"response after extract_nouns {response1}")
            result_string =' '.join(response1)
            print(result_string)
            updated_keyword = result_string
            
            print(f"updated_keyword --- {updated_keyword}")
        # Check if the language is English and the translation is the same as the original input
        # if lang.lower() == 'english':
        #     if  key_of_lang != 'en':
        #         print("Translation and user input are the same. Please rephrase.")
        #         dispatcher.utter_message(text="Your input and the translated text are the same. Please provide a different input or rephrase for better understanding.")
        #         return [FollowupAction("utter_price_details")]
        #     else:
        #         updated_keyword = translation 
            
            # if lang.lower() == 'english' and key_of_lang != 'en':
            #     print("Translation and user input are the same. Please rephrase.")
            #     dispatcher.utter_message(text="Your input and the translated text are the same. Please provide a different input or rephrase for better understanding.")
            #     return [FollowupAction("utter_price_details")]      
            # else:
            #     if lang.lower() != 'english':
            #         print("Different lang")
            #         print(f"key language from langTo eng function {key_of_lang}")
            #         slot_check = CheckKeywordAction()
            #         slot_set = slot_check.setLangSlot(key_of_lang)
            #         print(f" after slot set {slot_set}")
            #         lang_slot_value = tracker.get_slot("user_query_language")
            #         print(f"lang_slot_value ---> {lang_slot_value}")

            #     # Use the translated keyword for further processing
            #     updated_keyword = translation

        # Load the NLU training data
        nlu_data = self.load_nlu_data()
        res=[]
        res_domain_list=[]
        res_domain_value = tracker.get_slot("res_domain")
        res_domain = False
        #the nlu data has nlu file data in json format. 
        #this part access the domain details examples from the json data and it is stored in examples
        for intent_data in nlu_data:
            if "nlu" in nlu_data:
                for intent_data in nlu_data["nlu"]:
                    #checking only the domain details
                    if isinstance(intent_data, dict) and intent_data.get("intent") == "domain_details":
                        examples_str = intent_data.get("examples", "")
                        examples = examples_str.split("\n")
                        # print(f"exstr: {examples}")
                        # Remove hyphens from the examples
                        examples = [example.replace("- ", "") for example in examples]
                        # print(f"1 {keyword}")
                        # print(f"2 {examples}") 
                        object=allFunc()
                        #calling the check_words function here                  
                        result = object.check_words_in_intent(updated_keyword, examples)
                        print(f"domain list: {result}")  # True/False

                        res_domain_list.extend(result)
                        #RESULT - USED FOR BARD OUTPUT
                        # If the word comes from test fallback, it has to check if the word is there in the other intents
                        # so repeating the above steps for other intents in this function
                        #this is a list - that has true or false output for other intents
                        result_after_matching_list, intent_name = object.checking_other_intents(updated_keyword)
                        #an array of true or false is returned. 
                        # IF EEN ONE TRUE EXISTS IN THE ARRAY, SETTING THE VALUE TO TRUE
                        # IF NO TRUE EXISTS IN THE ARRAY, SETTING THE VAL TO FALSE
                        print(f"result_after_matching list {result_after_matching_list}")  # True/False
                        print(f"result_after_matching intent_name {intent_name}")  # True/False
                        item_price = None  # Initialize item_price outside of the block
                        # Check if intent_name is a list and has multiple elements
                        if isinstance(intent_name, list) and len(intent_name) > 1:
                            contains_item_details = False
                            contains_price_details = False
                            for item in intent_name:
                                if "item_details" in item:
                                    contains_item_details = True
                                if "price_details" in item:
                                    contains_price_details = True
                            
                            # Check if both item_details and price_details are present
                            if contains_item_details and contains_price_details:
                                print("True")
                                item_price = "True"
                            else:
                                print("False")
                                item_price = "False"

                            # print("Item price:", item_price)
                            print(f"Multiple elements: {intent_name}")
                            intent_name = "multiple"
                            print(f"Printing intent name multiple -- {intent_name}")
                        else:
                            intent_name = intent_name[0]
                            print(f"Single element: {intent_name}")
                            print(f"Printing intent name Single -- {intent_name}")

                        # HIS FOR LOOP CHECKS AND STORES THE OUTPUT IF THE VALUES PRESENT IN OTHER INTENTS

                        if not result_after_matching_list and not res_domain_list:
                            print("all the words are removed from the user message")
                            return[FollowupAction("utter_default_msg")]

                        for res in result_after_matching_list:
                            if res == True:
                                #set res value and stop
                                result_after_matching = True
                                break
                            else:
                                result_after_matching = False

        #inside domain value function also, each word is checked and returns true or false. so it also has to be store in an array so that
        #it will get redirect to defalt fallback directly. if no, the fst value(which is almost false) will be taken, and gets rediredted
        #to the "retail-specific" if part (output will Be still The same, buT user has to click the get more info btton.)
        
        for res in res_domain_list:
            if res==True:
                #seting domain value as true(came from default fallback)
                res_domain=True
                break
            else:
                res_domain=False

        # if res_domain == True and result_after_matching==False:

        # if res_domain == True and result_after_matching == True :
        #     res_domain == False 
        # if is_result_after_matching_list_empty == True:
        #     return [FollowupAction("utter_default_msg")] 
            if res_domain == True:   
                if result_after_matching == True:
                    if intent_name is None:
                        print(f"true true {intent_name}")
                        print(f"printing res_domain {res_domain}")
                        print(f"printing result_after_matching {result_after_matching}")
                        res_domain = True 
                        return [SlotSet("user_input_question_true", result_after_matching),SlotSet("res_domain", res_domain),SlotSet("getting_intent_name", intent_name),FollowupAction("action_default_fallback")]
                            # return [SlotSet("user_query_language", key_of_lang)]

                    else:
                        print(f"true true {intent_name}")
                        print(f"printing res_domain {res_domain}")
                        print(f"printing result_after_matching {result_after_matching}")
                        res_domain = True   
                        return [SlotSet("user_input_question_true", result_after_matching),SlotSet("res_domain", res_domain),SlotSet("getting_intent_name", intent_name),FollowupAction("utter_specific_use_case_and_general_domain")]
                    
                elif result_after_matching == False:
                    print(f"true false {intent_name}")
                    print(f"printing res_domain {res_domain}")
                    print(f"printing result_after_matching {result_after_matching}")
                    res_domain = True
                    go_to_bard = "go to bard"
                    print(f"inside redirecting if {go_to_bard}")

                    return[SlotSet("user_input_question", go_to_bard),SlotSet("res_domain", res_domain),FollowupAction("action_default_fallback")] 

            else:
                print(f"inside redirecting else - main {result_after_matching}")
                # IF ONE TRUE EXIST IN ARRAY, THEN IT IS DOMAIN SPECIFIC(Filtered)            
                if res_domain == False:
                    if result_after_matching == True:
                        user_entered_value = tracker.latest_message.get("text")
                        print(f"false true {intent_name}")
                        res_domain = False
                        print(f"printing res_domain {res_domain}")
                        print(f"printing result_after_matching {result_after_matching}")
                        print(f"user input {user_entered_value}")
                        return [SlotSet("user_input_question_true", result_after_matching),SlotSet("res_domain", res_domain),SlotSet("getting_intent_name", intent_name),FollowupAction("action_check_slot")] #, FollowupAction("action_check_slot")
                    elif result_after_matching==False:
                        res_domain = False
                        user_entered_value1 = tracker.latest_message.get("text")
                        # gemini_instance  = gemini_instance.Geminipro()
                        object=allFunc()
                        full_source_language_name, translation = object.translate_and_print_language(user_entered_value1)
                        # print(f"Source Language key: {lang_key}")
                        # print (f"full_source_language_name {full_source_language_name}")
                        # print(f"user input for synonym {translation}")
                        print(f"false false {intent_name}")
                        print(f"printing res_domain {res_domain}")
                        print(f"printing result_after_matching {result_after_matching}")

        # ----------------------------SYNONYMS FILTERING-------------------------------------------------------------
                        gemini_instance = Geminipro()
                        print("after gemini call")
                        # response = gemini_instance.send_message_and_get_response(user_entered_value1) 
                        # print("Model's response:", response)
                        # extract_keyword = gemini_instance.extract_keyword(response)
                        # print("Extracted Keyword:", extract_keyword)
                        # find_synonyms = gemini_instance.find_synonyms(extract_keyword)
                        # print("found synonym:", find_synonyms)
                        # object=allFunc()
                        # result= object.check_for_synonym_keywords(find_synonyms)
                        # print("before noun call")
# **********************************************************
                        # response1= gemini_instance.extract_nouns(translation)
                        # print("after noun call")
                        # print(f"response after extract_nouns {response1}")
# **********************************************************


                        # ------------------------------------------------------------

                        # user_input= "list all the synonym for today in retail"
                        # object=allFunc()
                        # response = object.palmApi(user_input)
                        # print("inside PALM3.....")
                        # if response == None:
                        #     print("inside palm response")
                        # else:
                        #     print(f"inside palm response -- {response}")

                        # ------------------------------------------------------------
                        if response1 is not None and len(response1) > 0:
                            words_array1 = response1  # Assuming response1 is your list of words
                            unique_words = list(set(words_array1))  # Removing duplicates
                            print(f"unique_words {unique_words}")

                            # user_input = f" {response1} in the array pick all the retail related word only no need any defintion just pick the retail related keyword from the array and give all the output in an array with retail words only "
                            user_input = f"Extract all retail-related keywords from the array {response1} and return a new array containing only those keywords."
                            object=allFunc()
                            response = object.palmApi(user_input)
                            print(f"palm taking retail keyword from user {response}")
                            #-------------- 
                            # Extracting the array from the response string
                            array_start_index = response.find("[")
                            array_end_index = response.rfind("]") + 1  # Include the closing bracket

                            if array_start_index != -1 and array_end_index != -1:
                                array_string = response[array_start_index:array_end_index]
                                array = ast.literal_eval(array_string)
                                print(f"printing the array - {array}")
                            else:
                                print("Array not found in the response")
                            # -------------
                            if response is None:
                                print("try again later!!!")
                            else:
                                print("inside noun call from palm" , array)
                                
                                # words_array1 = array  # Assuming response1 is your list of words
                                # print(f"words_array1 {words_array1}")
                                # print(f"word array1 type {type(words_array1)}")
                                # words_array2 = ast.literal_eval(words_array1)

                                for word in array:
                                    print(word)

                                # for word in words_array1:
                                #     print(f"Word: {word}")
                                    # Call the function to find synonyms for each word
                                    # find_synonyms = gemini_instance.find_synonyms(word)
                                    # # Further processing with synonyms if needed
                                    # if find_synonyms is not None:
                                    #     print(f"Synonyms for '{word}': {find_synonyms}")
                                    # else:
                                    #     print(f"No synonyms found for '{word}'")
                                # for word in words_array1:
                                #     print(''.join(word))
        # ----------------------
                            synonyms_combined = []
                            # array = []
        # ---------------------------------
                            # Printing each word individually
                            for word in array:
                                if word is None:
                                    synonyms_combined.extend(['sample', 'check'])  # Adding default values if find_synonyms is None
                                    # print("Combined synonyms array:", synonyms_combined)
                                else:                            
                                    find_synonyms = gemini_instance.find_synonyms(word)
                                    if find_synonyms is None:
                                        synonyms_combined.extend(['sample', 'check'])  # Adding default values if find_synonyms is None
                                        # print("Combined synonyms array:", synonyms_combined)
                                    else:
                                        print(f"found synonym for '{word}'---> {find_synonyms}")
                                        synonyms_combined.extend(find_synonyms)
                                        # print("Combined synonyms array:", synonyms_combined)
                        
                        else:  
                            print("No unique words found or response is empty.")
                            error_text = "I am not quite sure what you're asking.You can ask me anything related to retail domain, I will do my best to help you in any way that I can."
                            dispatcher.utter_message(text=error_text)
                            return [SlotSet("user_input_question_true", result_after_matching), SlotSet("res_domain", res_domain),FollowupAction("utter_price_details")]  

                        object=allFunc()
                        print("before check_for_synonym_keywords call")
                        result= object.check_for_synonym_keywords(synonyms_combined)
                        print("After check_for_synonym_keywords call")
                        print(f"result {result}")

                        # print("Model's response - 2:", response1) 
                        # extract_keyword1 = gemini_instance.extract_keyword(response1)
                        # print("Extracted Keyword -2 :", extract_keyword1)
                        # find_synonyms1 = gemini_instance.find_synonyms(extract_keyword1)
                        # print("found synonym - 2:", find_synonyms1)
                        # # object=allFunc()
                        # result1= object.check_for_synonym_keywords(find_synonyms1)
                        # print(f"second result-{result1}")

                # --------------------------------------FINAL RESULT---------------------------------------------------
                        # print(f"result {result}")
                        if result is None:
                            error_text = "I apologize, but it looks like the information that you are trying to get is not retail specific.\n\
                                    You can ask me anything related the domain, I will do my best to help you in any way that I can."      
                            dispatcher.utter_message(text=error_text)
                                    #setting this slot because, after setting this,chec if this vale is true in the slot and if yes, buttons has to be displayed
                            return [SlotSet("user_input_question_true", result_after_matching), SlotSet("res_domain", res_domain),FollowupAction("utter_price_details")]  
                        elif result == "none":
                                raw_user_input_to_check_isRetail = tracker.latest_message.get("text")
                                full_source_language_name, translation = object.translate_and_print_language(raw_user_input_to_check_isRetail)
                                print (f"full_source_language_name {full_source_language_name}")
                                print (f"translation {translation}")
                                updated_keyword = translation

                                check_user_input_isRetail = f"Is the phrase '{updated_keyword}' related to the retail domain? Please respond with a simple 'Yes' or 'No' without providing an explanation."
                                object=allFunc()
                                response = object.palmApi(check_user_input_isRetail)
                                print(f"Printing the Palm response for the user input to determine if it belongs to the retail domain: {response}")
                                if response == 'Yes' or response == 'yes':
                                    user_input= "Definition of " +updated_keyword+" in retail"
                                    object=allFunc()
                                    response = object.palmApi(user_input)
                                    if response == None:
                                        dispatcher.utter_message("Sorry, I couldn't generate a response for that input. Please try again with a different prompt.")
                                    else:
                                        print(response)
                                        dispatcher.utter_message(response)
                                    return[FollowupAction("action_check_slot")]
                                else:
                                    error_text = "I apologize, but it looks like the information that you are trying to get is not retail specific.\n\
                                                You can ask me anything related the domain, I will do my best to help you in any way that I can."      
                                    dispatcher.utter_message(text=error_text)
                                    return [SlotSet("user_input_question_true", result_after_matching), SlotSet("res_domain", res_domain),FollowupAction("utter_price_details")]  
                            # error_text = "I'm sorry, I didn't quite catch that. Could you please rephrase your question?"
                            # dispatcher.utter_message(text=error_text)
                            # return [SlotSet("user_input_question_true", result_after_matching), SlotSet("res_domain", res_domain),FollowupAction("utter_price_details")]  

                        elif result == "multiple" :
                            error_text = "It seems your query falls under multiple categories. Please rephrase your statement or select the below usecase"
                            dispatcher.utter_message(text=error_text)
                            return [SlotSet("user_input_question_true", result_after_matching), SlotSet("res_domain", res_domain),FollowupAction("utter_redisplay_buttons_nonretail")]

                        # elif result in ['Supplier','supplier'] :
                        elif re.search(r'supp', result, re.IGNORECASE):
                            print(f"inside supplier {result}")
                            message = "It seems like you are looking for information related to suppliers."
                            dispatcher.utter_message(text=message)
                            return [SlotSet("user_input_question_true", result_after_matching), SlotSet("res_domain", res_domain),FollowupAction("utter_supplier_number")]  
                        # elif result in ['order', 'Purchase order', 'PO', 'purchase order', 'Order']:
                        elif re.search(r'order', result, re.IGNORECASE):
                            message = "It seems like you are looking for information related to orders."
                            dispatcher.utter_message(text=message)
                            print(f"inside order {result}")
                            return [SlotSet("user_input_question_true", result_after_matching), SlotSet("res_domain", res_domain),FollowupAction("utter_order_number")]  
                        # elif result in [ 'Inventory','inventory']:
                        elif re.search(r'invent', result, re.IGNORECASE):
                            message = "It seems like you are looking for information related to inventory."
                            dispatcher.utter_message(text=message)
                            print(f"inside Inventory {result}")
                            return [SlotSet("user_input_question_true", result_after_matching), SlotSet("res_domain", res_domain),FollowupAction("utter_loc_for_inventory")]  
                        # elif result in ['Price','Prices']:
                        elif re.search(r'pric', result, re.IGNORECASE):
                            message = "It seems like you are looking for information related to pricing."
                            dispatcher.utter_message(text=message)
                            print(f"inside Price {result}")
                            return [SlotSet("user_input_question_true", result_after_matching), SlotSet("res_domain", res_domain),FollowupAction("utter_use_cases")]
                        elif re.search(r'item', result, re.IGNORECASE):
                            message = "It seems like you are looking for information related to item."
                            dispatcher.utter_message(text=message)
                            print(f"inside item {result}")
                            return [SlotSet("user_input_question_true", result_after_matching), SlotSet("res_domain", res_domain),FollowupAction("utter_item_number")]

                        # elif result is None:
                        #     error_text = "I'm sorry, I didn't quite catch that. Could you please rephrase your question?"
                        #     dispatcher.utter_message(text=error_text)
                        #     return [SlotSet("user_input_question_true", result_after_matching), SlotSet("res_domain", res_domain),FollowupAction("utter_price_details")]  
                        else:
                
                        # user_input_check= extract_keyword(user_entered_value1)
                        # IF NO TRUE EXISTS IN THE ARRAY, THEN IT IS NOT RETAIL SPECIFIC, RETURN ERROR MESSAGE
                                error_text = "I apologize, but it looks like the information that you are trying to get is not retail specific.\n\
                                    You can ask me anything related the domain, I will do my best to help you in any way that I can."      
                                dispatcher.utter_message(text=error_text)
                                    #setting this slot because, after setting this,chec if this vale is true in the slot and if yes, buttons has to be displayed
                                return [SlotSet("user_input_question_true", result_after_matching), SlotSet("res_domain", res_domain),FollowupAction("utter_price_details")]  
            # else:
            #     error_text = "I apologize, but it looks like the information that you are trying to get is not retail specific.\n\
            #                   You can ask me anything related the domain, I will do my best to help you in any way that I can."      
            #     dispatcher.utter_message(text=error_text)
        # user_query_language = tracker.get_slot("user_query_language")
        # print(f"user_query_language2: {user_query_language}")
        return [SlotSet("intent_name", intent_name)]

        #  C:\Users\yraja\LogicBot\local_test\data\nlu.yml
          
    def load_nlu_data(self):
        # Load the NLU training data from the nlu.yml file
        nlu_file_path=r"C:\Users\yraja\LogicBot\local_test\data\nlu.yml"
        # nlu_file_path="/app/data/nlu.yml"
        with open(nlu_file_path, "r") as file:
            return yaml.safe_load(file)
        

    def setLangSlot(self,slotVal):
        print(f"inside setLangSlot function {slotVal}")
        return [SlotSet("user_query_language", slotVal)]
    
#keeping the a"action_default_fallback" and "action_test_fallback" as it is, as, if suppose domain or nlu fallback gets hit directly, these two will work
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # if res_domain == True:   
            # if result_after_matching == True:
        get_res_domain_slot=tracker.get_slot("res_domain")
        print("get_res_domain_slot to print from bard",get_res_domain_slot)
        user_input=tracker.latest_message.get("text")
        if get_res_domain_slot == True:
            user_input=tracker.latest_message.get("text")
            if user_input:
                print("user_input ",user_input)
                print("get_res_domain_slot ",get_res_domain_slot)
                # if user_input=="Get Item Prices" or "Get Specific Price" or "Get Price at All Locs" or "get_item_prices" or "get_specific_price" or "get_item_all_locs":
                user_input= "Definition of " +user_input+" in retail"
                object=allFunc()
                response = object.palmApi(user_input)
                if response == None:
                    dispatcher.utter_message("Sorry, I couldn't generate a response for that input. Please try again with a different prompt.")
                else:
                    dispatcher.utter_message(response)
            return[FollowupAction("action_check_slot")] #FollowupAction("action_check_slot")
        # elif get_res_domain_slot == None:
        #     print("user_input ",user_input)
        #     print("get_res_domain_slot ",get_res_domain_slot) 
        #     dispatcher.utter_message("I'm here to assist with retail-related queries. If you have any questions or need help regarding retail, feel free to ask! Unfortunately, I might not be able to assist with other topics outside the retail domain.")
        #     return[FollowupAction("action_check_slot")]
        # elif get_res_domain_slot == False:
        #     print("user_input ",user_input)
        #     print("get_res_domain_slot ",get_res_domain_slot) 
        #     dispatcher.utter_message("I'm here to assist with retail-related queries. If you have any questions or need help regarding retail, feel free to ask! Unfortunately, I might not be able to assist with other topics outside the retail domain.")
        #     return[FollowupAction("action_check_slot")]    
        else:
            return[FollowupAction("action_check_slot")] #FollowupAction("action_check_slot")
        
        
    
        # # user_input = tracker.get_slot("user_input_question")
        # user_input=tracker.latest_message.get("text")
        # print(user_input) 
        # if user_input:
        #     user_input=user_input+" in retail"
        #     object=allFunc()
        #     response = object.call_chatgpt_api(user_input)
        #     dispatcher.utter_message(response)
        # dispatcher.utter_message("I apologize, but I am currently in development stage, so, I am not yet ready \n\
        #                             with the data that you expect. Please check back later.")

class ActionGoToBardMoreInfo(Action):
    def name(self) -> Text:
        return "action_toBard_with_previous_value"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        user_messages = [event['text'] for event in tracker.events if event['event'] == 'user']
        user_input = user_messages[-2] if len(user_messages) >= 2 else None  

        # #in the server, button click is redirected to this action. so dding this line for it tocheck if the button name is the etered text
        # #and run accordingly
        # if user_input:
        #     # if user_input=="Get Item Prices" or "Get Specific Price" or "Get Price at All Locs" or "get_item_prices" or "get_specific_price" or "get_item_all_locs":
        #     user_input=user_input+" in retail"
        #     object=allFunc()
        #     response = object.call_chatgpt_api(user_input)
        #     dispatcher.utter_message(response)

        # dispatcher.utter_message("I apologize, but I am currently in development stage, so, I am not yet ready \n\
        # #                             with the data that you expect. Please check back later.")

        if user_input:
            object=allFunc()
            full_source_language_name, translation = object.translate_and_print_language(user_input)
            print (f"full_source_language_name {full_source_language_name}")
            print (f"translation {translation}")
            updated_keyword = translation
                # if user_input=="Get Item Prices" or "Get Specific Price" or "Get Price at All Locs" or "get_item_prices" or "get_specific_price" or "get_item_all_locs":
            user_input= "Definition of " + updated_keyword + " in retail"
            print("*******BARD() check************ ")
            print(f"{user_input}")
            object=allFunc()
            response = object.palmApi(user_input)
            if response == None:
                dispatcher.utter_message("Sorry, I couldn't generate a response for that input. Please try again with a different prompt.")
            else:
                dispatcher.utter_message(response)
        return[SlotSet("user_input_question", "go to bard")]
        # except:
        #     print("the button name is taken as the text input")
        
    def load_nlu_data(self):
        # Load the NLU training data from the nlu.yml file
        nlu_file_path=r"C:\Users\yraja\LogicBot\local_test\data\nlu.yml"
        # nlu_file_path="/app/data/nlu.yml"
        with open(nlu_file_path, "r") as file:
            return yaml.safe_load(file)
        
class ActionTestFallback(Action):
    def name(self) -> Text:
        return "action_test_fallback"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        #redirecting to the check intent action, as, if the fallback gets hit wrongly and the word is retail specific, it has to go to bard        
        print("inside test fallback ,redirecting")
        return[FollowupAction('check_value_in_intent')]

class ActionCheckSlot(Action):
    def name(self) -> Text:
        return "action_check_slot"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        #since we have two different buttons o be displayed, we have two slots to check, and accordingly buttons has to be displayed. 
        #so the story has to be written for two slots seprately,and we need this action.
        slotVal=tracker.get_slot("user_input_question")
        slotVal1=tracker.get_slot("user_input_question_true")
        slot_value1 = tracker.get_slot("getting_intent_name")
        res_domain_value = tracker.get_slot("res_domain")
        

        #goto bard will get set only if it goes to the bard if condition in the check slot action. 
        #which means user_input_question will not have a value, so it will considered as none here.
        #in some cases, like consignment item - consignment is not usecase specific so it is true, but item is usecase specific, so overall it has 
        #prioritize the true fnction and has to display all the 5 buttons.
        if  res_domain_value == False and slotVal1 == True:
        #the word is domain specific, but not an usecase
            slot_value1 = tracker.get_slot("getting_intent_name") # order_details
            user_entered_value = tracker.latest_message.get("text") # user message

            sup1=tracker.get_slot('numeric_values')  # display what is inside numeric_value slot
            if slot_value1 == "order_details+user_entered_numeric_values" or slot_value1 == "order_details":
                    user_entered_value = tracker.latest_message.get("text") # user message
                    print('type of user input',type(user_entered_value))
                    # Use regular expression to extract numbers
                    numbers = re.findall(r'\d+', user_entered_value)
                    # numbers1 = re.findall(r'\b(\d+)\b', user_entered_value)
                    # Convert the extracted numbers to integers (if needed)
                    numeric_values = [int(number) for number in numbers]
                    print('variable to store',numbers)
                    for i in numeric_values:
                        print('value in list', i) 
                    print('final variable to store',numeric_values)

                    # print('5.slotvalue inside supplier',slot_value1)
                    # print('6.inside supplier if',sup1)
                    if not numeric_values:
                        print('empty list')
                        return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_order_Notification")]
                    else:
                        print('Non empty list')
                        order_num = tracker.get_slot("supplier_with_number")
                        print('value in slot',order_num)
                        return [SlotSet("user_input_question_true", slotVal),SlotSet("order_with_number", i),FollowupAction("action_order_with_number_details")]
            elif slot_value1 == "supplier_details+user_entered_numeric_values" or slot_value1 == "supplier_details":
                    user_entered_value = tracker.latest_message.get("text") # user message
                    print('type of user input',type(user_entered_value))
                    # Use regular expression to extract numbers
                    numbers = re.findall(r'\d+', user_entered_value)
                    # numbers1 = re.findall(r'\b(\d+)\b', user_entered_value)
                    # Convert the extracted numbers to integers (if needed)
                    numeric_values = [int(number) for number in numbers]
                    print('variable to store',numbers)
                    for i in numeric_values:
                        print('vlaue in list', i) 
                    print('final variable to store',numeric_values)

                    print('5.slotvalue inside supplier',slot_value1)
                    print('6.inside supplier if',sup1)
                    if not numeric_values:
                        print('empty list')     
                        return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_supplier_Notification")]
                        # return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_supplier_number")]
                    else:
                        print('Non empty list')
                        supplier_num = tracker.get_slot("supplier_with_number")
                        print('value in slot',supplier_num)
                        return [SlotSet("user_input_question_true", slotVal),SlotSet("supplier_with_number", i),FollowupAction("action_supplier_with_number_details")]

            elif slot_value1 == "inventory_details":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_inventory_Notification")]
            elif slot_value1 == "asking_help":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_price_details")]
            # elif slot_value1 == "price_details":
            #     return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_use_cases")]
            elif slot_value1 == "price_details" and user_entered_value == "Get Item Prices":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("action_all_item_prices")]
            elif slot_value1 == "price_details" and user_entered_value == "Get Price at All Location":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("action_utter_display_prev_item_uc3")]
            elif slot_value1 == "price_details" and user_entered_value == "Get Specific Price":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("action_utter_display_prev_item")]
            elif slot_value1 == "price_details" or user_entered_value == "price details":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_price_Notification")]
            elif slot_value1 == "inventory_loc_type1":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("action_inventory_details_for_wh")]
            elif slot_value1 == "inventory_loc_type2":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("action_inventory_details_for_store")]
            elif slot_value1 == "deny":
                msg = "Not a problem! If you ever change your mind or have more questions in the future, don't hesitate to return. I'm here to assist you whenever you need it."
                dispatcher.utter_message(text=msg)
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_price_details")]
            elif slot_value1 == "name":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_name")]
            elif slot_value1 == "greet":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_greet")]
            elif slot_value1 == "feeling_intent":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_how_are_you")]
            elif slot_value1 == "ask_whatspossible":
                msg = "I'm here to provide information, answer questions, and assist you with your queries related to the retail domain."
                dispatcher.utter_message(text=msg)
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_session_started"),FollowupAction("utter_price_details")]        
            elif slot_value1 == "hello":
                msg = "Welcome to Logic Retail Bot. Please feel free to ask queries related to the below usecases. I am here to assist you."
                dispatcher.utter_message(text=msg)
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_session_started"),FollowupAction("utter_price_details")]
            elif slot_value1 == "affirm":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_session_started"),FollowupAction("utter_price_details")]
            elif slot_value1 == "ask_whatismyname":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_session_started"),FollowupAction("utter_name")]
            elif slot_value1 == "leave":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_session_started"),FollowupAction("Action_new_features")]
            elif slot_value1 == "hello":
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_session_started"),FollowupAction("utter_session_started")]
            elif slot_value1 == "item_details":  
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_item_Notification")]
            elif slot_value1 == "multiple": 
                # if item_price == "True":
                    # return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_price_Notification")]
                msg="It seems your query falls under multiple categories. Please rephrase your statement."
                dispatcher.utter_message(text=msg)
                return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_price_details")]
            # elif slot_value1 == "supplier_details+user_entered_numeric_values":
            #     return [SlotSet("user_input_question_true", slotVal),FollowupAction("action_supplier_with_number_details")]
            
            elif slot_value1 == "continue_info" or slot_value1 == "/continue_info" or slot_value1 == "repeat the same scenario":
                prev_action_name = None
                second_prev_action_name = None
                third_prev_action_name = None
                fourth_prev_action_name = None
                fifth_prev_action_name = None
                sixth_prev_action_name = None
                seventhth_prev_action_name = None
                eighth_prev_action_name = None
                ninthth_prev_action_name = None
                tenth_prev_action_name = None
                eleventth_prev_action_name = None
                twelth_prev_action_name = None
                # Loop through the events to find the previous and multiple previous action names
                for event in reversed(tracker.events):
                    if event.get("event") == "action":
                        if prev_action_name is None:
                            prev_action_name = event.get("name")
                        elif second_prev_action_name is None:
                            second_prev_action_name = event.get("name")
                        elif third_prev_action_name is None:
                            third_prev_action_name = event.get("name")
                        elif fourth_prev_action_name is None:
                            fourth_prev_action_name = event.get("name")
                        elif fifth_prev_action_name is None:
                            fifth_prev_action_name = event.get("name")
                        elif sixth_prev_action_name is None:
                            sixth_prev_action_name = event.get("name")
                        elif seventhth_prev_action_name is None:
                            seventhth_prev_action_name = event.get("name")
                        elif eighth_prev_action_name is None:
                            eighth_prev_action_name = event.get("name")
                        elif ninthth_prev_action_name is None:
                            ninthth_prev_action_name = event.get("name")
                        elif tenth_prev_action_name is None:
                            tenth_prev_action_name = event.get("name")
                        elif eleventth_prev_action_name is None:
                            eleventth_prev_action_name = event.get("name")
                        elif twelth_prev_action_name is None:
                            twelth_prev_action_name = event.get("name")      
                        else:
                            break

                # Now you have the second, third, fourth, and fifth previous action names
                # if fifth_prev_action_name:                
                if prev_action_name: 
                    print(f"Previous action: {prev_action_name}")
                    print(f"Second previous action: {second_prev_action_name}")
                    print(f"Third previous action: {third_prev_action_name}")
                    print(f"Fourth previous action: {fourth_prev_action_name}")
                    print(f"Fifth previous action: {fifth_prev_action_name}")
                    print(f"6 action: {sixth_prev_action_name}")
                    print(f"7 previous action: {seventhth_prev_action_name}")
                    print(f"8 previous action: {eighth_prev_action_name}")
                    print(f"9 previous action: {ninthth_prev_action_name}")
                    print(f"10 previous action: {tenth_prev_action_name}")
                    print(f"11 action: {eleventth_prev_action_name}")
                    print(f"12 previous action: {twelth_prev_action_name}")
            
                    if fifth_prev_action_name == "action_supplier_details":
                        return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_supplier_number")]
                    elif fifth_prev_action_name == "action_order_details":
                        return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_order_number")]
                    elif fifth_prev_action_name == "action_inventory_details_for_store":
                        return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_loc_for_inventory")]
                    elif fifth_prev_action_name == "action_inventory_details_for_wh":
                        return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_loc_for_inventory")]
                    elif fifth_prev_action_name == "action_all_item_prices":
                        return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_item_buttons_repeat")]
                    elif fifth_prev_action_name == "action_get_pricedetail":
                        return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_item_buttons_repeat")]
                    elif fifth_prev_action_name == "action_getPrice_at_All_Location":
                        return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_item_buttons_repeat")]
                    elif fifth_prev_action_name == "action_getPrice_at_All_Location":
                        return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_item_buttons_repeat")]
                    else:
                        dispatcher.utter_message("I apologize, but it looks like the information that you are trying to get is not retail specific. You can ask me anything related the domain, I will do my best to help you in any way that I can.")
                        return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_price_details")]
                else:
                    print("outside else")
                    return [SlotSet("user_input_question_true", slotVal),FollowupAction("utter_price_details")]
        elif  res_domain_value == False and slotVal1 == False : 
            slot_value1 = tracker.get_slot("getting_intent_name")
            print("inside action check slot false false")
            dispatcher.utter_message(template="utter_price_details")


        elif res_domain_value == True:   
        # elif res_domain_value == True or slotVal1 == True:
        # else:
        #should now got to the bard, no need of get more info button, so it will display the price details
            print(f"\n\n slotVal inside else {slotVal1}")
            slot_value1 = tracker.get_slot("getting_intent_name")
            # dispatcher.utter_message(text=f"The value in the slot(else) is: {slotVal1}")
            # dispatcher.utter_message(text=f"The value in the slot(else) is: {slotVal}")
            # dispatcher.utter_message(text=f"The value in the slot(else) is: {slot_value1}")
            # dispatcher.utter_message(text=f"The value in the slot(domain else) is: {res_domain_value}")

            # text3 = "testing inside else"
            # slot_value3 = tracker.get_slot("getting_intent_name")
            # dispatcher.utter_message(text=f"The value in the slot(else) is: {slot_value3}")
            # dispatcher.utter_message(text=text3)
            # dispatcher.utter_message(text=f"Inside else go to bard")

            # error_text = "I apologize, but 
            # it looks like the information that you are trying to get is NOT retail specific.\n\
            #         You can ask me anything related the domain, I will do my best to help you in any way that I can."      
            # dispatcher.utter_message(text=error_text)
            print("inside elif")
            dispatcher.utter_message(template="utter_price_details")

        #the function gets over here,so the slots are made none for the next iteration - if needed, set the slot with necessary values
        #KEEP THE RETURN STATEMENT OUTSIDE THE IF SO THAT ALL THE SLOTS GET SET TO NONE AGAIN, ONCE THE ACTION IS COMPLETED.
        #EVEN IF THE SLOTS ARE NOT SET PROPERLY, HAVING A COMMON RETURN FOR NONE CAN HELP.

            # return[SlotSet("user_input_question_true", None), SlotSet("user_input_question", None)]
            return[SlotSet("user_input_question_true", None), SlotSet("user_input_question", None)]

        else:
            print("inside else ........")
            # dispatcher.utter_message("I apologize, but it looks like the information that you are trying to get is not retail specific. You can ask me anything related the domain, I will do my best to help you in any way that I can.")
            dispatcher.utter_message(template="utter_price_details")
            return[SlotSet("user_input_question_true", None), SlotSet("user_input_question", None)]        
        # # else:
        # #should now got to the bard, no need of get more info button, so it will display the price details
        #     print(f"\n\n slotVal inside else {slotVal1}")
        #     slot_value1 = tracker.get_slot("getting_intent_name")
        #     # dispatcher.utter_message(text=f"The value in the slot(else1) is: {slotVal1}")
        #     # dispatcher.utter_message(text=f"The value in the slot(else1) is: {slotVal}")
        #     # dispatcher.utter_message(text=f"The value in the slot(else1) is: {slot_value1}")
        #     # dispatcher.utter_message(text=f"The value in the slot(domain else1) is: {res_domain_value}")

        #     # text3 = "testing inside else"
        #     # slot_value3 = tracker.get_slot("getting_intent_name")
        #     # dispatcher.utter_message(text=f"The value in the slot(else) is: {slot_value3}")
        #     # dispatcher.utter_message(text=text3)
        #     # dispatcher.utter_message(text=f"Inside else go to bard")

        #     # error_text = "I apologize, but 
        #     # it looks like the information that you are trying to get is NOT retail specific.\n\
        #     #         You can ask me anything related the domain, I will do my best to help you in any way that I can."      
        #     # dispatcher.utter_message(text=error_text)
        #     dispatcher.utter_message(template="utter_price_details")
        # #the function gets over here,so the slots are made none for the next iteration - if needed, set the slot with necessary values
        # #KEEP THE RETURN STATEMENT OUTSIDE THE IF SO THAT ALL THE SLOTS GET SET TO NONE AGAIN, ONCE THE ACTION IS COMPLETED.
        # #EVEN IF THE SLOTS ARE NOT SET PROPERLY, HAVING A COMMON RETURN FOR NONE CAN HELP.
        #     return[SlotSet("user_input_question_true", None), SlotSet("user_input_question", None)]      
        #  
class HandleNumericValues(Action):
    def name(self) -> Text:
        return "action_handle_numeric_values"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the user's message
        message = tracker.latest_message.get("text")
        print(message)
        special_characters_pattern = r'[+*?-^%^]'

        # Check if the message contains special characters
        if re.search(special_characters_pattern, message):
            dispatcher.utter_message("I'm sorry, I can't perform mathematical operations.")
            return []
        else:
            dispatcher.utter_message("I'm sorry, I can't perform mathematical operations.")
            return []
        
class UtterDefaultMessage(Action):
    def name(self):
        return "action_default_msg"

    def run(self, dispatcher, tracker, domain):
        # Define the response you want to send
        message = "Sorry, I didn't get that 🤷. Could you please rephrase?"
        # Use the dispatcher to send the message
        dispatcher.utter_message(text=message)
        return []
    

class ValidatePredefinedSlots(ValidationAction):
    def validate_supplier_value(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate numeric_values value."""
        if isinstance(slot_value, str):
            # Use a regular expression to extract numeric part from the input
            numeric_part = re.search(r'\d+', slot_value)
            if numeric_part:
                extracted_number = numeric_part.group()
                print("extracted",extracted_number)
                return {"supplier_value": extracted_number}
            else:
                print("No numeric part found, set the slot to None") 
                return {"supplier_value": None}
        else:
            print("validation failed, set this slot to None") 
            return {"supplier_value": None}


class ActionWelcomeMessage(Action):

    def name(self) -> Text:
        return "Action_Welcome_Message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Welcome to Logic Retail Bot. Please feel free to ask queries related to the below usecases. I am here to assist you.")
        return [FollowupAction("utter_price_details")]


class ActionNewFeatures(Action):

    def name(self) -> Text:
        return "Action_new_features"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Hello 😀")  

        dispatcher.utter_message(text="Here is something to cheer you up 😉", image="https://b.zmtcdn.com/data/pictures/1/17428541/da50010b1a953dfbb109306fba5a6c06.jpg") 

        return [FollowupAction("Action_new_features2")]


class ActionNewFeatures2(Action):

    def name(self) -> Text:
        return "Action_new_features2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # button in utter 
         
        # Videos
        video = { "type": "video", "payload": { "title": "Link name", "src": "https://youtube.com/embed/9C1Km6xfdMA" } }

        dispatcher.utter_message(text="Check this video",attachment=video)

        return [FollowupAction("Action_new_features3")]
    

class ActionNewFeatures3(Action):
    def name(self) -> Text:
        return "Action_new_features3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # # Quick reply
        # data= [ { "title":"chip1", "payload":"chip1_payload" }, { "title":"chip2", "payload":"chip2_payload" }, { "title":"chip3", "payload":"chip3_payload" } ]

        # message={"payload":"quickReplies","data":data}

        # dispatcher.utter_message(text="Please choose a cuisine",json_message=message)

        # # Dropdown
        # data=[{"label":"option1","value":"/inform{'slot_name':'option1'}"},{"label":"option2","value":"/inform{'slot_name':'option2'}"},{"label":"option3","value":"/inform{'slot_name':'option3'}"}]

        # message={"payload":"dropDown","data":data}
  
        # dispatcher.utter_message(text="Please select a option",json_message=message)

        return [FollowupAction("Action_new_features4")]



class ActionNewFeatures4(Action):
    def name(self) -> Text:
        return "Action_new_features4"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        # collapsible

        data= [ { "title": "Sick Leave", "description": "Sick leave is time off from work that workers can use to stay home to address their health and safety needs without losing pay." }, { "title": "Earned Leave", "description": "Earned Leaves are the leaves which are earned in the previous year and enjoyed in the preceding years. " }, { "title": "Casual Leave", "description": "Casual Leave are granted for certain unforeseen situation or were you are require to go for one or two days leaves to attend to personal matters and not for vacation." }, { "title": "Flexi Leave", "description": "Flexi leave is an optional leave which one can apply directly in system at lease a week before." } ]

        message={ "payload": "collapsible", "data": data }

        dispatcher.utter_message(text="You can apply for below leaves",json_message=message)

        # charts
        data1={ "title": "Leaves", "labels": [ "Sick Leave", "Casual Leave", "Earned Leave", "Flexi Leave" ], "backgroundColor": [ "#36a2eb", "#ffcd56", "#ff6384", "#009688", "#c45850" ], "chartsData": [ 5, 10, 22, 3 ], "chartType": "pie", "displayLegend": "true" }

        message={ "payload": "chart", "data": data1 }

        dispatcher.utter_message(text="Here are your leave balance details",json_message=message)

        return [FollowupAction("Action_new_features5")]


class ActionNewFeatures5(Action):
    def name(self) -> Text:
        return "Action_new_features5"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # cards_carousel 
        
        data2 = {
                "payload": 'cardsCarousel',
                "data": [
                    {
                        "image": "https://b.zmtcdn.com/data/pictures/1/18602861/bd2825ec26c21ebdc945edb7df3b0d99.jpg",
                        "title": "Taftoon Bar & Kitchen",
                        "ratings": "4.5",
                    },
                    {
                        "image": "https://b.zmtcdn.com/data/pictures/4/18357374/661d0edd484343c669da600a272e2256.jpg",

                        "ratings": "4.0",
                        "title": "Veranda"
                    },
                    {
                        "image": "https://b.zmtcdn.com/data/pictures/4/18902194/e92e2a3d4b5c6e25fd4211d06b9a909e.jpg",

                        "ratings": "4.0",
                        "title": "145 The Mill"
                    },
                    {
                        "image": "https://b.zmtcdn.com/data/pictures/3/17871363/c53db6ba261c3e2d4db1afc47ec3eeb0.jpg",

                        "ratings": "4.0",
                        "title": "The Fatty Bao"
                    },
                ]
            }

        dispatcher.utter_message(json_message=data2)

        # pdf attachmnet

        data3 = {
            "payload": "pdf_attachment",
            "title": "PDF Title",
            "url": "C:/Users/yraja/LogicBot/local_test/docs/sup_20.pdf"
        }
        dispatcher.utter_message(text="Check this PDF", attachment=data3)

        return [FollowupAction("utter_price_details")]
    
  
class ActionCheckForRetailDomain(Action):
    def name(self) -> Text:
        return "action_check_for_retial_domain"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
 
            user_input=tracker.latest_message.get("text")
            if user_input:
                print("user_input ",user_input)
                user_input= "Definition of " +user_input+" in retail"
                object=allFunc()
                response = object.palmApi(user_input)
                if response == None:
                    dispatcher.utter_message("Sorry, I couldn't generate a response for that input. Please try again with a different prompt.")
                else:
                    dispatcher.utter_message(response)
            return[FollowupAction("action_check_slot")]


# # download  chat as file
# class ActionDownloadFile(Action):
#     def name(self) -> Text:
#         return "action_download_file"
#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
        
#         dispatcher.utter_message("Here is he output file.")
#         # download_as_file
#         # last_bot_response = tracker.events[-2].get('text', None)  # Assuming the last bot response is in the second-to-last event
#         fileObj = jsonConversion()
#         last_bot_response = fileObj.compiled_array_return()
#         print(f"last_bot_response: {last_bot_response}")
#         if last_bot_response:
#             # Sample data
#             # item_data = [
#             #     {"bot_response": last_bot_response},
#             # ]
#             object=allFunc()
#             file_url,filename=object.download_as_file(last_bot_response)
#             if last_bot_response:
#                 dispatcher.utter_message(
#                         text=f"Click [here]({file_url}) to download the file.",
#                         attachment={
#                             "name": filename,
#                             "data": file_url
#                         }
#                     )
#         else:
#             dispatcher.utter_message(text="Cannot download file as no data is found.")
#             return[]

    

# from rasa_sdk import Action
# from rasa_sdk.events import SlotSet
# class ReadIntentsAction(Action):
#     def name(self):
#         return "check_value_in_intent"
#     def run(self, dispatcher, tracker, domain):
#         self.set_the_slot(tracker)
#         keyword=tracker.get_slot("user_input_question")
#         # Read the NLU data from the domain file
#         nlu_data = domain.get('intents', [])
#         # Find the "domain_details" intent
#         domain_details_intent = None
#         # for intent in nlu_data:
#         #     if intent.get('name') == 'domain_details':
#         #         domain_details_intent = intent
#         #         break
#         # Read the NLU data from the domain file
#         nlu_data = domain.get('intents', [])
#         # Find the "domain_details" intent
#         domain_details_intent = next(
#             (intent for intent in nlu_data if intent.get('name') == 'domain_details'),
#             None
#         )
#         if domain_details_intent:
#             # Extract the words from the "domain_details" intent examples
#             examples = domain_details_intent.get('examples', [])
#             words = set()
#             for example in examples:
#                 words.update(example.split())
#             if keyword in words:
#                 print("exist")
#             # Set a slot with the words for further use
#             return [FollowupAction(ActionDefaultFallback)]
#         else:
#             print(f"inside else part: {keyword}")
#             dispatcher.utter_message("I apologize for the inconvenience, but it looks like the information that you are trying to get is not retail specific.\n")
#             dispatcher.utter_message("You can ask me anything related the domain, I will do my best to help you in any way that I can.")
#             return [SlotSet("user_input_question", None)]
    
    # def set_the_slot(self, tracker: Tracker) -> List[Dict[Text, Any]]:
    #     entity_value = next(tracker.get_latest_entity_values("user_input_question"), None)
    #     print(f"entity value {entity_value}")
    #     return [SlotSet("user_input_question", entity_value)]
        