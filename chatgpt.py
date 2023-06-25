# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai

openai.api_key = "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"


def prompting(content):
    content = "Please create the Brief History of the Property and how the Owner /mortgagor has derived Title" + \
        content
    outputFormat = "I need the output in below format.Please start the response with a sentence like It appears from the deed and document under examination that and every history point should be alternatively start with thereafter and after that." + \
        "I need the response without any bullet points. I need the reponse with full address for every point." + \
        "every land measurement point should mention" "Piece and parcel of land measuring about more or less and registration details will have the following things in Capital  B of Book Number, V of Volume and P of Pages and B of being number or D of deed number" + \
        "Please complete the whole document"
    print("Executing chatgpt")
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[

            {"role": "user", "content": content},
            {"role": "user", "content": outputFormat}
        ]
    )
    print(result)
    if (result.choices[0].finish_reason == "length"):
        print("calling for length")
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[

                {"role": "user", "content": "Please continue for rest of the section"},
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
