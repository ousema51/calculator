from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/solve", methods=["POST"])
def solve():
    data = request.json

    return jsonify({
        "problem": data.get("problem"),
        "steps": ["Backend received request successfully"],
        "answer": "Test OK"
    })

if __name__ == "__main__":
    app.run()


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
