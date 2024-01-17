# # from nltk.corpus import wordnet

# # def get_synonyms(word):
# #     synonyms = set()
# #     for syn in wordnet.synsets(word):
# #         for lemma in syn.lemmas():
# #             synonyms.add(lemma.name())
# #     return list(synonyms)

# # def get_synonyms_for_word(word):
# #     synonyms = get_synonyms(word)
# #     synonyms_str = ', '.join(synonyms) if synonyms else "No synonyms found"
# #     return f"Synonyms for '{word}': {synonyms_str}"

# # # Example usage:
# # user_input = "supplier"  # Replace this with the user input you want to find synonyms for
# # synonyms_message = get_synonyms_for_word(user_input)
# # print(synonyms_message)

# import requests
# from bs4 import BeautifulSoup

# def get_synonyms(word):
#     url = f"https://www.thesaurus.com/browse/{word}"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, "html.parser")
#         synonyms_tag = soup.find("ul", {"class": "css-1lc0dpe et6tpn80"})
        
#         if synonyms_tag:
#             synonyms = [syn.text.strip() for syn in synonyms_tag.find_all("a")]
#             return synonyms
    
#     return []

# def get_synonyms_for_word(word):
#     synonyms = get_synonyms(word)
#     synonyms_str = ', '.join(synonyms) if synonyms else "No synonyms found"
#     return f"Synonyms for '{word}': {synonyms_str}"

# # Example usage:
# user_input = "vendor"  # Replace this with the user input you want to find synonyms for
# synonyms_message = get_synonyms_for_word(user_input)
# print(synonyms_message)
# --------------------------------------------------------------------------------------------

# import requests
# from bs4 import BeautifulSoup

# def get_synonyms(word):
#     url = f"https://www.thesaurus.com/browse/{word}"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, "html.parser")
#         synonyms_tag = soup.find("ul", {"class": "css-1lc0dpe et6tpn80"})
        
#         if synonyms_tag:
#             synonyms = [syn.text.strip() for syn in synonyms_tag.find_all("a")]
#             return synonyms
    
#     return []

# def store_synonyms_in_file(word, file_name):
#     synonyms = get_synonyms(word)
#     if synonyms:
#         with open(file_name, 'w') as file:
#             file.write(f"Synonyms for '{word}':\n")
#             for synonym in synonyms:
#                 file.write(f"{synonym}\n")
#         print(f"Synonyms for '{word}' stored in {file_name}")
#     else:
#         print(f"No synonyms found for '{word}'")

# # Example usage:
# user_input = "supplier"  # Replace this with the word you want to find synonyms for
# file_name = "supplier_synonyms.txt"  # Name of the file to store synonyms
# store_synonyms_in_file(user_input, file_name)


# give me synonyms for  the word VENDOR, in retail.
 
# is this VENDOR, in general, as a definition, closely related to purchase order? - yes or no - yes only if it is closely related - no if it is not closely related or not directly related.
 
# is this VENDOR, in general, as a definition, closely related to Inventory? - yes or no - yes only if it is closely related - no if it is not closely related or not directly related.
    
# is this VENDOR, in general, as a definition, closely related to pricing? - yes or no - yes only if it is closely related - no if it is not closely related or not directly related.
 
# is this VENDOR, in general, as a definition, closely related to Supplier? - yes or no - yes only if it is closely related - no if it is not closely related or not directly related.


# --------------------------------------------------------------------

from textblob import TextBlob
import nltk
def extract_nouns(sentence):
    # Create a TextBlob object
    blob = TextBlob(sentence)
 
    # Extract nouns using the pos_tags property
    nouns = [word for word, pos in blob.tags if pos.startswith('N')]
 
    return nouns
 
# Example usage
sentence = "I'm interested in learning more about the source of your materials."
nouns = extract_nouns(sentence)
 
print("Nouns:", nouns)
 