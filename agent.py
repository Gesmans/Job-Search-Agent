import anthropic
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# This is your connection to Claude
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
print(os.getenv("ANTHROPIC_API_KEY"))  # Debug: Check if API key is loaded correctly
messages=[]

print("Job Search Agent — type 'quit' to exit\n")
while True:
    # User Input
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break
    
    messages.append({"role": "user", "content": user_input})

    # Generate Response
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=messages
    )
    reply = ""
    for block in response.content:
        if block.type == "text":
            reply += block.text 
    
    # Add Claude's reply to history
    messages.append({"role": "assistant", "content": reply})
    
    print(f"\nAgent: {reply}\n")
