import requests

api_key = ""   # Your key here
model = "mistralai/mistral-7b-instruct"  # Or "openai/gpt-3.5-turbo" or "meta-llama/llama-3-8b-instruct"

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
data = {
    "model": model,
    "messages": [
        {"role": "user", "content": "Tell me a fun fact about AI."}
    ]
}

response = requests.post(url, headers=headers, json=data)
response_json = response.json()
if "choices" in response_json:
    print(response_json["choices"][0]["message"]["content"])
else:
    print("Error or unexpected response:", response_json)
