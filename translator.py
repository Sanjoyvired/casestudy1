from googletrans import Translator
from chatgpt import translator


def chunk_string(text, chunk_size=1000):
    start_index = 0
    end_index = min(len(text), chunk_size)

    while start_index < len(text):
        chunk = text[start_index:end_index]

        # Check if the chunk ends within a word or sentence
        if end_index < len(text):
            while text[end_index] != ' ' and text[end_index] != '.' and text[end_index] != '।':
                end_index -= 1
                if end_index <= start_index:
                    break

        yield chunk

        # Move the start and end index to the next chunk
        start_index = end_index + 1
        end_index = min(start_index + chunk_size, len(text))

        # If all chunks have been processed, return None
        if start_index >= len(text):
            return None


def translate(text):
    # Initialize the translator
    translator = Translator(service_urls=['translate.google.com'])

# Bengali text to be translated
    bengali_text = text

# Translate Bengali text to English
    translation = translator.translate(bengali_text, src='bn', dest='en')

# Print the translated text
    return (translation.text)


def translatorWrapper(text):
    # Example usage
    bengali_text = text
    chunk_generator = chunk_string(bengali_text)
    final_result = ""
    count = 1
    print("starting the translator#################")

    while True:
        try:
            chunk = next(chunk_generator)

            count = count+1
            # print(chunk)

            result = translator(chunk)
            # print(result)
            print(count)
            final_result += result
        except StopIteration:
            break

    print("Ending the translator")
    return final_result
