# # import googletrans
# # import translate 
# # import deepl 
# # from googletrans import Translator
# # print(googletrans.LANGUAGES) # to know all available languages

# # text1 = "எனக்கு சப்ளையர் தகவல் தேவை" 
# text1 = "I need supplier info" 
# text2 = "أحتاج إلى معلومات المورد"
# text3 = "j'ai besoin d'informations sur le fournisseur"
# text4 = " मुझे आपूर्तिकर्ता की जानकारी चाहिए "

# # translator = Translator()

# # print(translator.detect(text1))
# # print(translator.detect(text2))
# # print(translator.detect(text3))

# import langid
# from googletrans import Translator

# print(langid.classify(text1))
# print(langid.classify(text2))
# print(langid.classify(text3))
# print(langid.classify(text4))

# def translate_to_english(text):
#     lang, confidence = langid.classify(text)
#     if confidence > 0.1:  # Adjust confidence threshold as needed
#         translator = Translator()
#         translation = translator.translate(text, src=lang, dest='en')
#         return translation.text
#     else:
#         return "Language identification confidence too low."

# text_to_translate = "مرحبا بك في العالم"
# translated_text = translate_to_english(text_to_translate)
# print(translated_text)






# -------------------------------TRANSLATION-----------------------------------------

from googletrans import Translator, LANGUAGES
translator = Translator()
# user_input = 'أحتاج إلى معلومات المورد'

from googletrans import Translator, LANGUAGES

translator = Translator()
# user_input = 'أحتاج إلى معلومات المورد'
user_input = f"بحاجة إلى معلومات المورد"


translation = translator.translate(user_input, dest='en')

full_source_language_name = LANGUAGES.get(translation.src)

print(f"Source Language: {full_source_language_name}")
print(f"Translated Text: {translation.text}")

print(translation)

# ----------------- LANGUAGE DETECTION ----------------------------------------
# from googletrans import Translator
# translator = Translator()
# print(f"1-------------------------------------")
# print(translator.detect(f"'bihajat 'iilaa maelumat almawrid'"))
# # <Detected lang=ko confidence=0.27041003>
# print(f"2-------------------------------------")
# print(translator.detect('この文章は日本語で書かれました。'))
# # <Detected lang=ja confidence=0.64889508>
# print(f"3-------------------------------------")
# print(translator.detect('This sentence is written in English.'))
# # <Detected lang=en confidence=0.22348526>
# print(f"4-------------------------------------")
# print(translator.detect('Tiu frazo estas skribita en Esperanto.'))
# # <Detected lang=eo confidence=0.10538048>
# print(f"5-------------------------------------")
# print(translator.detect('எனக்கு சப்ளையர் தகவல் தேவை'))
# print(f"6-------------------------------------")
# print(translator.detect('ennaku supplier thagaval thevai'))
# print(f"7-------------------------------------")
# print(translator.detect('أحتاج إلى معلومات المورد'))
# print(f"8-------------------------------------")
# print(translator.detect('ahtaj iilaa maelumat almawrid'))
# print(f"9-------------------------------------")
# print(translator.detect('मुझे आपूर्तिकर्ता की जानकारी चाहिए'))
# print(f"10-------------------------------------")
# print(translator.detect('mujhe aapoortikarta kee jaanakaaree chaahie'))
# print(f"11-------------------------------------")
# print(translator.detect(f"'j'ai besoin d'informations sur le fournisseur'"))
# print(f"12-------------------------------------")
# print(translator.detect('ฉันต้องการข้อมูลซัพพลายเออร์'))
# print(f"13-------------------------------------")
# print(translator.detect('C̄hạn t̂xngkār k̄ĥxmūl sạphphlāy xe xr̒'))


# ---------------------------------------------------------