import os
from openai import OpenAI

# Constants
SYSTEM_PROMPT_PATH = 'data/system_prompt.txt'
FINE_TUNED_MODEL = "ft:gpt-4o-mini-2024-07-18:personal::9xVBMAYR"

def load_system_prompt():
    with open(SYSTEM_PROMPT_PATH, 'r') as file:
        return file.read().strip()

def chat_with_gpt():
    client = OpenAI()
    
    system_prompt = load_system_prompt()
    messages = [{"role": "system", "content": system_prompt}]

    print("Welcome to the Terminal ChatGPT Application!")
    print("Using fine-tuned model:", FINE_TUNED_MODEL)
    print("Type 'quit' to exit the chat.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model=FINE_TUNED_MODEL,
                messages=messages
            )
            assistant_response = response.choices[0].message.content
            print(f"\nAssistant: {assistant_response}")
            messages.append({"role": "assistant", "content": assistant_response})
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    chat_with_gpt()
