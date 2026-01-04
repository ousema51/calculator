from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
@app.route("/solve", methods=["POST"])
def solve():
    try:
        data = request.get_json()

        problem = data.get("problem", "").strip()
        mode = data.get("mode", "derivative")
        limit_point = data.get("limitPoint")

        if not problem:
            return jsonify({"error": "No problem provided"}), 400

        prompt = f"""
Solve this math problem step by step.

Mode: {mode}
Problem: {problem}
Limit point: {limit_point}

Return the result in this JSON format ONLY:
{{
  "problem": "...",
  "steps": ["step 1", "step 2"],
  "answer": "final answer"
}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content

        return jsonify(eval(content))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def health():
    return "Backend is running"
