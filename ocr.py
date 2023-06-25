from PIL import Image
import cv2
import pytesseract
import os
import chatgpt
import translator


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


# Function to perform OCR on an image given its file path

def ocr_image(image_path, language):
    # Open the image using PIL (Python Imaging Library)
    image = Image.open(image_path)
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(image, lang=language)

    # Return the extracted text
    return text
# code for breaking a string


# Specify the path to the document folder
folder_path = 'Document'
language = "eng"

# Initialize a variable to store the consolidated result
consolidated_result = ""

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    print("Start Processing")
    # Check if the file is an image
    if filename.endswith('.jpeg') or filename.endswith('.png'):
        # Get the full path of the image file
        image_path = os.path.join(folder_path, filename)

        # Perform OCR on the image file
        result_text = ocr_image(image_path, language)

        # Append the result to the consolidated output
        consolidated_result += result_text

# Print the consolidated result
# print(consolidated_result)

if (language != "eng"):

    # calling translation service
    # consolidated_result = break_string(consolidated_result, 100)
    # print(consolidated_result)

    consolidated_result = translator.translatorWrapper(consolidated_result)
print("Consolidated Result")
print(consolidated_result)
# calling chat Gpt
print("Executing the summarizer")
final = chatgpt.prompting(consolidated_result)
print(final)
