import openai 

#Configuration with LLM model 
openai.api_base = "http://localhost:1234/v1"
openai.api_key = "not-needed"

def LLM_interation(
        user_input: str,
        system_message: str
    ):
    messages = [
                    {
                        "role": "system",
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
    return openai.ChatCompletion.create(
                model = "local model",
                messages = messages,
                temperature = 0.7
            )

def main(user_input=None):
    #Define system message
    system_message = (
                "The user name of this function is Ayumu Yamamoto but I prefer to be called Joey. I am doing a project on carbon footprints from different cars and I want you to be my assistant in this project. "
                "I want to gather information about carbon emission of different car brands and car models. "
                "Whenever I ask you any question about carbon emission of different models, keep you answers concise and precise. "
                "Maintan a friendly and respectful tone in your responses. Polietly correct me if I am wrong at any stage. "
            )
    
    while True:
        
        if user_input == None:
            user_input = input("User: " )

        if user_input.lower() in ['exit', 'bye', 'end']:
            print("Exiting the chat boat")
            break

        message = LLM_interation(
                        user_input = user_input, 
                        system_message = system_message
                    )
        print("Model response:", message.choices[0].message.content)
        return message.choices[0].message.content

if __name__ == "__main__":
    main()