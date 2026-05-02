import anthropic
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

messages = []

# This is your connection to Claude
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

userName = input("What is your Name? ").strip()

def AIAgent():
    print(f"Hello, {userName}! I am your Job Search Agent. I will analyze your CV and find potential job opportunities for you.")
    print("Do you want to proceed with analyzing your CV? (yes/no)")
    user_input = input().strip().lower()

    if user_input == "yes":
        with open('cv.txt', 'r') as file:
                cv_content = file.read()
                system_prompt = f"You are a Job search agent. Your task is to analyze the provided CV and generate a list of potential job opportunities that match the skills and experience outlined in {cv_content}. You should extract skills from the CV, search for jobs posted within the last 3 days, and score them. Only find mid to senior level roles. Provide a list of the top 5 job opportunities with a brief description and a link to the job posting. If you cannot find any relevant job opportunities, please respond with 'No relevant job opportunities found.'"
        while True:
                user_input = input("You: ")
                if user_input.lower() == "exit":
                    print("Exiting the Job Search Agent. Goodbye!")
                    break

                messages.append({"role": "user", "content": user_input})

                response = client.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=1024,
                    system=system_prompt,
                    tools=[{"type": "web_search_20250305", "name": "web_search"}],
                    messages=messages
                )

                reply = ""
                for block in response.content:
                    if block.type == "text":
                        reply += block.text 

                print(f"Claude: {reply}")

                messages.append({"role": "assistant", "content": reply})


    elif user_input == "no":
        print("No problem! If you change your mind, just let me know.")
        exit()
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
        exit()

    

if __name__ == "__main__":
    AIAgent()

