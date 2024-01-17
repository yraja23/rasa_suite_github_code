from langdetect import detect

text = 'بحاجة إلى معلومات المورد'
detected_lang = detect(text)
print(detected_lang)  # Output: ar (Arabic)
