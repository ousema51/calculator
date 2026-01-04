from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy import symbols, diff, limit, integrate, sympify
from sympy.core.sympify import SympifyError

app = Flask(__name__)

# ✅ Allow ALL origins, ALL methods, ALL headers
CORS(app, resources={r"/*": {"origins": "*"}})

x = symbols("x")

@app.route("/solve", methods=["POST", "OPTIONS"])
def solve():
    if request.method == "OPTIONS":
        return "", 200  # ✅ THIS FIXES PREFLIGHT

    try:
        data = request.get_json(force=True)

        mode = data.get("mode")
        problem = data.get("problem")
        limit_point = data.get("limitPoint")

        if not problem or not mode:
            return jsonify({"error": "Missing input"}), 400

        try:
            expr = sympify(problem)
        except SympifyError:
            return jsonify({
                "problem": problem,
                "steps": [],
                "answer": "Invalid expression. Use * for multiplication (example: 3*x)"
            })

        steps = []

        if mode == "derivative":
            steps.append("Differentiate with respect to x")
            result = diff(expr, x)

        elif mode == "limit":
            if limit_point is None:
                return jsonify({
                    "problem": problem,
                    "steps": [],
                    "answer": "Limit point required"
                })
            steps.append(f"Compute limit as x → {limit_point}")
            result = limit(expr, x, limit_point)

        elif mode == "integral":
            steps.append("Integrate with respect to x")
            result = integrate(expr, x)

        else:
            return jsonify({"error": "Invalid mode"}), 400

        return jsonify({
            "problem": problem,
            "steps": steps,
            "answer": str(result)
        })

    except Exception as e:
        return jsonify({
            "problem": "",
            "steps": [],
            "answer": "Backend error"
        }), 500
