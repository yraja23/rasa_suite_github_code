# """
# At the command line, only need to run once to install the package via pip:

# $ pip install google-generativeai
# """

# import google.generativeai as genai

# genai.configure(api_key="AIzaSyAxAkTbuGGD7yJeIPqU7pi-RpEZSXIudRQ")

# # Set up the model
# generation_config = {
#   "temperature": 0.9,
#   "top_p": 1,
#   "top_k": 1,
#   "max_output_tokens": 2048,
# }

# safety_settings = [
#   {
#     "category": "HARM_CATEGORY_HARASSMENT",
#     "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#   },
#   {
#     "category": "HARM_CATEGORY_HATE_SPEECH",
#     "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#   },
#   {
#     "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#     "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#   },
#   {
#     "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#     "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#   },
# ]

# model = genai.GenerativeModel(model_name="gemini-pro",
#                               generation_config=generation_config,
#                               safety_settings=safety_settings)

# convo = model.start_chat(history=[
#   {
#     "role": "user",
#     "parts": "hi"
#   },
#   {
#     "role": "model",
#     "parts": "Hello! How can I assist you today?"
#   },
#   {
#     "role": "user",
#     "parts": "give me all maximum possible synonyms for  the word VENDOR, in retail."
#   },
#   {
#     "role": "model",
#     "parts": "Here is a comprehensive list of maximum possible synonyms for the word VENDOR in retail:\n\n* Retailer\n* Seller\n* Merchant\n* Shopkeeper\n* Storekeeper\n* Tradesperson\n* Purveyor\n* Supplier\n* Provider\n* Distributor\n* Huckster\n* Monger\n* Dealer\n* Peddler\n* Boutiquier\n* Concessionaire\n* Franchisee\n* Kiosk operator\n* Market vendor\n* Pop-up shop owner\n* Street vendor\n* Chandlery\n* Chandler\n* Costermonger\n* Factor\n* Haberdasher\n* Hawker\n* Importer\n* Ironmonger\n* Jackleg\n* Jobber\n* Merchandiser\n* Mongrel\n* Outfitter\n* Retailer\n* Sales associate\n* Salesclerk\n* Salesman\n* Salesperson\n* Salesrep\n* Shop assistant\n* Shop girl\n* Shopkeep\n* Store clerk\n* Storeman\n* Sutler\n* Trader\n* Trafficker\n* Vendor\n\nThis list is by no means exhaustive, as there are many other words that could be used to describe a vendor in retail, depending on the specific context. However, these are some of the most common and widely used synonyms.\n\nI hope this helps!"
#   },
#   {
#     "role": "user",
#     "parts": "give me all maximum possible synonyms for  the word invoice , in retail domain"
#   },
#   {
#     "role": "model",
#     "parts": "Here is a comprehensive list of maximum possible synonyms for the word INVOICE in the retail domain:\n\n* Bill\n* Statement\n* Tab\n* Check\n* Receipt\n* Sales slip\n* Purchase order\n* Packing slip\n* Delivery note\n* Credit memo\n* Debit memo\n* Proforma invoice\n* Commercial invoice\n* Customs invoice\n* Tax invoice\n* Cash sale invoice\n* Charge slip\n* Sales ticket\n* Bill of sale\n* Itemized statement\n* Statement of account\n\nIn addition to the above, here are some more specific synonyms for INVOICE in the retail domain, depending on the context:\n\n* POS receipt - a receipt printed by a point-of-sale (POS) system at the time of purchase.\n* Electronic invoice (e-invoice) - an invoice that is sent electronically, typically via email or EDI.\n* Self-billing invoice - an invoice that is created by the customer, rather than the vendor.\n* Recurring invoice - an invoice that is generated and sent on a regular basis, such as monthly or annually.\n* Final invoice - an invoice that is sent after all goods or services have been delivered and all payments have been made.\n\nI hope this list is helpful!"
#   },
#   {
#     "role": "user",
#     "parts": "give me all maximum possible synonyms for  the word stock , in retail."
#   },
#   {
#     "role": "model",
#     "parts": "Here is a comprehensive list of maximum possible synonyms for the word STOCK in retail:\n\n* Inventory\n* Merchandise\n* Goods\n* Products\n* Items\n* Commodities\n* Assortment\n* Selection\n* Range\n* Line\n* Offering\n\nIn addition to the above, here are some more specific synonyms for STOCK in retail, depending on the context:\n\n* Fast-moving stock - stock that sells quickly and easily.\n* Slow-moving stock - stock that sells slowly or not at all.\n* Dead stock - stock that is no longer selling and is unlikely to sell in the future.\n* Overstock - stock that is in excess of what is needed to meet current demand.\n* Backstock - stock that is stored in a warehouse or stockroom, rather than on the sales floor.\n* Safety stock - stock that is held in reserve to meet unexpected demand or to protect against stockouts.\n* Seasonal stock - stock that is only sold during certain times of the year.\n* Promotional stock - stock that is sold at a reduced price or with special promotions.\n* Clearance stock - stock that is being sold at a reduced price to make room for new stock.\n\nI hope this list is helpful!"
#   },
#   {
#     "role": "user",
#     "parts": "give me all maximum possible synonyms for  the word pricing, in retail."
#   },
#   {
#     "role": "model",
#     "parts": "Here is a comprehensive list of maximum possible synonyms for the word PRICING in retail:\n\n* Costing\n* Rate-setting\n* Valuing\n* Figuring\n* Estimating\n* Quoting\n* Assessing\n* Appraising\n* Charging\n* Demanding\n* Asking\n\nIn addition to the above, here are some more specific synonyms for PRICING in retail, depending on the context:\n\n* Markdown - a reduction in the price of an item, typically to clear out old stock or to make room for new stock.\n* Markup - an increase in the price of an item, typically to cover the cost of goods sold and to make a profit.\n* Suggested retail price (SRP) - the price that a manufacturer recommends that a retailer sell a product for.\n* Everyday low price (EDLP) - a pricing strategy in which a retailer keeps its prices low every day, rather than having sales or discounts.\n* High-low pricing - a pricing strategy in which a retailer offers high prices on some items and low prices on other items, in order to attract a wide range of customers.\n* Price skimming - a pricing strategy in which a retailer sets a high price for a new product, then gradually lowers the price over time.\n* Penetration pricing - a pricing strategy in which a retailer sets a low price for a new product in order to quickly gain market share.\n* Bundle pricing - a pricing strategy in which a retailer offers a group of products together at a discounted price.\n* Dynamic pricing - a pricing strategy in which a retailer adjusts its prices frequently, based on factors such as demand, competition, and the cost of goods sold.\n\nI hope this list is helpful!"
#   },
#   {
#     "role": "user",
#     "parts": "give me synonyms for  the word VENDOR, in retail."
#   },
#   {
#     "role": "model",
#     "parts": "Here are some synonyms for the word VENDOR in retail:\n\n* Retailer\n* Seller\n* Merchant\n* Shopkeeper\n* Storekeeper\n* Tradesperson\n* Purveyor\n* Supplier\n* Provider\n* Distributor\n* Huckster\n* Monger\n* Dealer\n* Peddler\n\nIn addition to the above, here are some more specific synonyms for VENDOR in retail, depending on the context:\n\n* Boutiquier - a vendor who owns or operates a boutique, a small, fashionable store.\n* Concessionaire - a vendor who operates a concession, a small booth or stand in a larger store or public space.\n* Franchisee - a vendor who owns and operates a franchise, a business that is part of a larger chain.\n* Kiosk operator - a vendor who operates a kiosk, a small, freestanding booth or stand.\n* Market vendor - a vendor who sells goods at a market, a temporary or permanent gathering of vendors.\n* Pop-up shop owner - a vendor who operates a pop-up shop, a temporary retail store.\n* Street vendor - a vendor who sells goods on the street, typically from a cart or stand.\n\nI hope this helps!"
#   },
# ])

# # convo.send_message("")
# # print(convo.last.text)


# user_input = "give me all maximum possible synonyms for  the word VENDOR, in retail."  # Replace this with your user input
# convo.send_message(user_input)
# model_response = convo.last.text

# # Storing the model's response in a variable
# stored_response = model_response

# # Printing or using the stored response
# print("output for supplier", stored_response)
# ------------------------------------------------------------------------------------------------------------

"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google_auth_oauthlib
from textblob import TextBlob
import yaml
import google.generativeai as genai
import time
import datetime
# AIzaSyAxAkTbuGGD7yJeIPqU7pi-RpEZSXIudRQ --YR
# AIzaSyBbc7JgiMLNOvTFLparUqH62TqPtkHpyvE - Meenatchi
# AIzaSyBCNdp_YJZAljw80e8qL87fVqbux2eJWP8
class Geminipro:
  genai.configure(api_key="AIzaSyDunsMXggY0kt-UvXYf2XQywBMx-4purvg")

  # Set up the model
  generation_config = {
    "temperature": 0.9, 
    "top_p": 1,
    "top_k": 1,
    # "max_output_tokens": 300,
    "max_output_tokens": 2048,

  }

  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
  ]

  model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

  convo = model.start_chat(history=[
    {
      "role": "user",
      "parts": "hi"
    },
    {
      "role": "model",
      "parts": "Hello! How can I assist you today?"
    },
    {
      "role": "user",
      "parts": "give me all maximum possible synonyms for  the word VENDOR, in retail."
    },
    {
      "role": "model",
      "parts": "Here is a comprehensive list of maximum possible synonyms for the word VENDOR in retail:\n\n* Retailer\n* Seller\n* Merchant\n* Shopkeeper\n* Storekeeper\n* Tradesperson\n* Purveyor\n* Supplier\n* Provider\n* Distributor\n* Huckster\n* Monger\n* Dealer\n* Peddler\n* Boutiquier\n* Concessionaire\n* Franchisee\n* Kiosk operator\n* Market vendor\n* Pop-up shop owner\n* Street vendor\n* Chandlery\n* Chandler\n* Costermonger\n* Factor\n* Haberdasher\n* Hawker\n* Importer\n* Ironmonger\n* Jackleg\n* Jobber\n* Merchandiser\n* Mongrel\n* Outfitter\n* Retailer\n* Sales associate\n* Salesclerk\n* Salesman\n* Salesperson\n* Salesrep\n* Shop assistant\n* Shop girl\n* Shopkeep\n* Store clerk\n* Storeman\n* Sutler\n* Trader\n* Trafficker\n* Vendor\n\nThis list is by no means exhaustive, as there are many other words that could be used to describe a vendor in retail, depending on the specific context. However, these are some of the most common and widely used synonyms.\n\nI hope this helps!"
    },
    {
      "role": "user",
      "parts": "give me all maximum possible synonyms for  the word invoice , in retail domain"
    },
    {
      "role": "model",
      "parts": "Here is a comprehensive list of maximum possible synonyms for the word INVOICE in the retail domain:\n\n* Bill\n* Statement\n* Tab\n* Check\n* Receipt\n* Sales slip\n* Purchase order\n* Packing slip\n* Delivery note\n* Credit memo\n* Debit memo\n* Proforma invoice\n* Commercial invoice\n* Customs invoice\n* Tax invoice\n* Cash sale invoice\n* Charge slip\n* Sales ticket\n* Bill of sale\n* Itemized statement\n* Statement of account\n\nIn addition to the above, here are some more specific synonyms for INVOICE in the retail domain, depending on the context:\n\n* POS receipt - a receipt printed by a point-of-sale (POS) system at the time of purchase.\n* Electronic invoice (e-invoice) - an invoice that is sent electronically, typically via email or EDI.\n* Self-billing invoice - an invoice that is created by the customer, rather than the vendor.\n* Recurring invoice - an invoice that is generated and sent on a regular basis, such as monthly or annually.\n* Final invoice - an invoice that is sent after all goods or services have been delivered and all payments have been made.\n\nI hope this list is helpful!"
    },
    {
      "role": "user",
      "parts": "give me all maximum possible synonyms for  the word stock , in retail."
    },
    {
      "role": "model",
      "parts": "Here is a comprehensive list of maximum possible synonyms for the word STOCK in retail:\n\n* Inventory\n* Merchandise\n* Goods\n* Products\n* Items\n* Commodities\n* Assortment\n* Selection\n* Range\n* Line\n* Offering\n\nIn addition to the above, here are some more specific synonyms for STOCK in retail, depending on the context:\n\n* Fast-moving stock - stock that sells quickly and easily.\n* Slow-moving stock - stock that sells slowly or not at all.\n* Dead stock - stock that is no longer selling and is unlikely to sell in the future.\n* Overstock - stock that is in excess of what is needed to meet current demand.\n* Backstock - stock that is stored in a warehouse or stockroom, rather than on the sales floor.\n* Safety stock - stock that is held in reserve to meet unexpected demand or to protect against stockouts.\n* Seasonal stock - stock that is only sold during certain times of the year.\n* Promotional stock - stock that is sold at a reduced price or with special promotions.\n* Clearance stock - stock that is being sold at a reduced price to make room for new stock.\n\nI hope this list is helpful!"
    },
    {
      "role": "user",
      "parts": "give me all maximum possible synonyms for  the word pricing, in retail."
    },
    {
      "role": "model",
      "parts": "Here is a comprehensive list of maximum possible synonyms for the word PRICING in retail:\n\n* Costing\n* Rate-setting\n* Valuing\n* Figuring\n* Estimating\n* Quoting\n* Assessing\n* Appraising\n* Charging\n* Demanding\n* Asking\n\nIn addition to the above, here are some more specific synonyms for PRICING in retail, depending on the context:\n\n* Markdown - a reduction in the price of an item, typically to clear out old stock or to make room for new stock.\n* Markup - an increase in the price of an item, typically to cover the cost of goods sold and to make a profit.\n* Suggested retail price (SRP) - the price that a manufacturer recommends that a retailer sell a product for.\n* Everyday low price (EDLP) - a pricing strategy in which a retailer keeps its prices low every day, rather than having sales or discounts.\n* High-low pricing - a pricing strategy in which a retailer offers high prices on some items and low prices on other items, in order to attract a wide range of customers.\n* Price skimming - a pricing strategy in which a retailer sets a high price for a new product, then gradually lowers the price over time.\n* Penetration pricing - a pricing strategy in which a retailer sets a low price for a new product in order to quickly gain market share.\n* Bundle pricing - a pricing strategy in which a retailer offers a group of products together at a discounted price.\n* Dynamic pricing - a pricing strategy in which a retailer adjusts its prices frequently, based on factors such as demand, competition, and the cost of goods sold.\n\nI hope this list is helpful!"
    },
    {
      "role": "user",
      "parts": "give me synonyms for  the word VENDOR, in retail."
    },
    {
      "role": "model",
      "parts": "Here are some synonyms for the word VENDOR in retail:\n\n* Retailer\n* Seller\n* Merchant\n* Shopkeeper\n* Storekeeper\n* Tradesperson\n* Purveyor\n* Supplier\n* Provider\n* Distributor\n* Huckster\n* Monger\n* Dealer\n* Peddler\n\nIn addition to the above, here are some more specific synonyms for VENDOR in retail, depending on the context:\n\n* Boutiquier - a vendor who owns or operates a boutique, a small, fashionable store.\n* Concessionaire - a vendor who operates a concession, a small booth or stand in a larger store or public space.\n* Franchisee - a vendor who owns and operates a franchise, a business that is part of a larger chain.\n* Kiosk operator - a vendor who operates a kiosk, a small, freestanding booth or stand.\n* Market vendor - a vendor who sells goods at a market, a temporary or permanent gathering of vendors.\n* Pop-up shop owner - a vendor who operates a pop-up shop, a temporary retail store.\n* Street vendor - a vendor who sells goods on the street, typically from a cart or stand.\n\nI hope this helps!"
    },
  ])

  # convo.send_message("")
  # print(convo.last.text)

  # --------------------------
  # user_input = "'i need to know my vendor information' extract the one main keyword from the text given"  # Replace this with your user input
  # # user_input = "give me all maximum possible synonyms for  the word Vendor information, in retail."
  # convo.send_message(user_input)
  # model_response = convo.last.text

  # # Storing the model's response in a variable
  # stored_response = model_response

  # # Printing or using the stored response
  # print("output for supplier", stored_response)

  # ------------------------------------


  def send_message_and_get_response(self, user_input):
    try:
      parsed_input = f"'{user_input}' - extract one main keyword from the text given"
      self.convo.send_message(parsed_input)
      model_response = self.convo.last.text
      print(f"model_response - {model_response}")
      return model_response
    
    except Exception  as e:
        print(f"Error: {e}")
    # raise RuntimeError("Failed to get response with multiple retries")

  def extract_keyword(self,response):
      start_marker = "**"
      end_marker = "**"
      start_index = response.find(start_marker)
      end_index = response.find(end_marker, start_index + len(start_marker))

      if start_index != -1 and end_index != -1:
          extracted_keyword = response[start_index + len(start_marker):end_index].strip()
          # print(f"extracted_keyword - {extracted_keyword}")
          return extracted_keyword
      else:
          return None

  def find_synonyms(self,keyword):
      user_input_synonyms = f"give me all maximum possible synonyms for  the word {keyword}, in retail."
      gemini_instance.convo.send_message(user_input_synonyms)
      model_response_synonyms = gemini_instance.convo.last.text
      extracted_synonyms = gemini_instance.extract_synonyms(model_response_synonyms)
      # print(f"extracted_synonyms - {extracted_synonyms}")
      return extracted_synonyms
  
  def extract_synonyms(self,response):
      start_marker = "\n* "
      end_marker = "\n\n"
      start_index = response.find(start_marker)
      end_index = response.find(end_marker, start_index + len(start_marker))

      if start_index != -1 and end_index != -1:
          synonyms_section = response[start_index + len(start_marker):end_index].strip()
          synonyms_list = synonyms_section.split("\n* ")
          # print(f"synonyms_list - {synonyms_list}")
          return synonyms_list
      else:
          return None

  def extract_nouns(self,sentence):
      blob = TextBlob(sentence)
      for word, pos in blob.tags:
        print(f"{word}: {pos}")
      retail_keywords = [word for word, pos in blob.tags if pos.startswith('NN') or pos.startswith('JJ')]

        # Filter out 'i' and words with less than 3 characters
      retail_keywords = [word for word in retail_keywords if word.lower() != 'i' and len(word) > 2 ]

      return retail_keywords

gemini_instance = Geminipro()




  # start_marker = "**"
  # end_marker = "**"
  # start_index = stored_response.find(start_marker)
  # end_index = stored_response.find(end_marker, start_index + len(start_marker))

  # if start_index != -1 and end_index != -1:
  #     extracted_keyword = stored_response[start_index + len(start_marker):end_index].strip()
  #     print("Extracted keyword:", extracted_keyword)
  # else:
  #     print("Keyword not found in the output.")
      
  # extracted_keyword = extract_keyword(stored_response)
  # if extracted_keyword:
  #     print("Extracted keyword:", extracted_keyword)
  # else:
  #     print("Keyword not found in the output.")
# ------------------------------------
# user_input = "'i need to know my vendor information' extract the one main keyword from the text given"
# stored_response = gemini_instance.send_message_and_get_response(gemini_instance.convo, user_input)
# print("output for supplier", stored_response)

# extracted_keyword = gemini_instance.extract_keyword(stored_response)
# if extracted_keyword:
#     print("Extracted keyword:", extracted_keyword)
#     synonyms = gemini_instance.find_synonyms(extracted_keyword)
#     if synonyms:
#         print("Synonyms:", synonyms)
#     else:
#         print("Synonyms not found.")
# else:
#     print("Keyword not found in the output.")