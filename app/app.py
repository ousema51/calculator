from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy import symbols, diff, limit, integrate, sympify
from sympy.core.sympify import SympifyError

app = Flask(__name__)
CORS(app)

x = symbols("x")


@app.route("/solve", methods=["POST"])
def solve():
    try:
        data = request.get_json()

        mode = data.get("mode")
        problem = data.get("problem")
        limit_point = data.get("limitPoint")

        if not problem or not mode:
            return jsonify({"error": "Missing problem or mode"}), 400

        # Convert string to sympy expression
        try:
            expr = sympify(problem)
        except SympifyError:
            return jsonify({
                "problem": problem,
                "steps": [],
                "answer": "Invalid expression. Use * for multiplication (example: 3*x)"
            })

        steps = []

        # ---------------- DERIVATIVE ----------------
        if mode == "derivative":
            steps.append("Apply derivative rules")
            result = diff(expr, x)

        # ---------------- LIMIT ----------------
        elif mode == "limit":
            if limit_point is None:
                return jsonify({
                    "problem": problem,
                    "steps": [],
                    "answer": "Please specify a limit point"
                })

            steps.append(f"Compute the limit as x → {limit_point}")
            result = limit(expr, x, limit_point)

        # ---------------- INTEGRAL ----------------
        elif mode == "integral":
            steps.append("Apply integration rules")
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
            "answer": "Error solving problem"
        })
