import anthropic

# This is your connection to Claude
client = anthropic.Anthropic(api_key='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')

# This sends message to claude and gets a response
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Search for Product Manager jobs in London"},
        {"role": "assistant", "content": "Here are some jobs I found..."},
        {"role": "user", "content": "What was the first job you found?"}
    ],
    tools=[
        {
            "type": "web_search_20250305",
            "name": "web_search",
            
        }
    ]
)

for block in response.content:
    if block.type == "text":
        print(block.text)
