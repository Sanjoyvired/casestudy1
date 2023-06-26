# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai

openai.api_key = "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"


def prompting(content):
    content = "Please create the Brief History of the Property and how the Owner /mortgagor has derived Title" + \
        content
    outputFormat = "need the output in below format." + \
        "I need the reponse with full address to be taken" + \
        "every land measurement point should mention Piece and parcel of land measuring about more or less and registration details will have the following things first letter in Capital Book Number,Volume and Pages and being number or deed number" + \
        "Please complete the whole text and the response should be written in concise manner"
    print("Executing chatgpt")
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[

            {"role": "user", "content": content},
            {"role": "user", "content": outputFormat}
        ]
    )
    print(result)
    return result.choices[0].message.content


def translator(content):
    content = "Please convert the following bengali language content to english"+content
    print("Executing translator chatgpt")
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[

            {"role": "user", "content": content},
        ]
    )
    return (result.choices[0].message.content)


def formatter(content):
    content = "you are a copywriter. Please format the below content so that it can be pasted in a word doc. " + content
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[

            {"role": "user", "content": content},
        ]
    )
    return (result.choices[0].message.content)
