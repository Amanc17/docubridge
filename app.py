import os
import pandas as pd
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Paste your OpenRouter API key here
OPENROUTER_API_KEY = "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"  # Replace with your key
MODEL = "mistralai/mistral-7b-instruct"  # Or "openai/gpt-3.5-turbo" etc.

def ask_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=data)
    rjson = response.json()
    if "choices" in rjson:
        return rjson["choices"][0]["message"]["content"]
    else:
        return f"Error or unexpected response: {rjson}"

@app.route("/", methods=["GET", "POST"])
def index():
    ai_answer = None
    error = None
    if request.method == "POST":
        try:
            file = request.files["file"]
            user_question = request.form["user_question"]
            if file.filename.endswith(".csv"):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)

            # Create a data summary for the prompt
            columns = ', '.join(df.columns)
            summary = f"The table has columns: {columns}.\n"
            summary += f"First 2 rows: {df.head(2).to_dict(orient='records')}\n"

            prompt = (
                f"Here is a table of data:\n{summary}"
                f"The user asks: {user_question}\n"
                "Please answer based only on the data above."
            )

            ai_answer = ask_llm(prompt)

        except Exception as e:
            error = f"Error: {str(e)}"
    return render_template("index.html", ai_answer=ai_answer, error=error)

if __name__ == "__main__":
    app.run(debug=True)