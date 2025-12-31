from flask import Flask, request, jsonify
from flask_cors import CORS

from sympy import symbols, sympify, diff, integrate, limit, oo

app = Flask(__name__)
CORS(app)  # allow frontend access

x = symbols('x')

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()

    mode = data.get("mode")
    problem = data.get("problem")

    if not mode or not problem:
        return jsonify({
            "problem": problem,
            "steps": ["Missing mode or problem."],
            "answer": "Error"
        }), 400

    try:
        # -------- DERIVATIVE --------
        if mode == "derivative":
            expr = sympify(problem)
            result = diff(expr, x)

            return jsonify({
                "problem": problem,
                "steps": [
                    "Apply differentiation rules.",
                    f"The derivative is {result}."
                ],
                "answer": str(result)
            })

        # -------- INTEGRAL --------
        elif mode == "integral":
            expr = sympify(problem)
            result = integrate(expr, x)

            return jsonify({
                "problem": problem,
                "steps": [
                    "Apply integration rules.",
                    f"The integral is {result} + C."
                ],
                "answer": f"{result} + C"
            })

        # -------- LIMIT --------
        elif mode == "limit":
            if "," not in problem:
                return jsonify({
                    "problem": problem,
                    "steps": [
                        "Limits must be written as: expression, point",
                        "Example: sin(x)/x, 0"
                    ],
                    "answer": "Invalid limit format"
                })

            expr_str, point_str = problem.split(",", 1)
            expr = sympify(expr_str.strip())

            point_str = point_str.strip()
            if point_str == "oo":
                point = oo
            elif point_str == "-oo":
                point = -oo
            else:
                point = sympify(point_str)

            result = limit(expr, x, point)

            return jsonify({
                "problem": problem,
                "steps": [
                    f"Identify the expression: {expr}",
                    f"Evaluate the limit as x → {point}.",
                    f"The limit equals {result}."
                ],
                "answer": str(result)
            })

        # -------- INVALID MODE --------
        else:
            return jsonify({
                "problem": problem,
                "steps": ["Invalid mode selected."],
                "answer": "Error"
            }), 400

    except Exception as e:
        return jsonify({
            "problem": problem,
            "steps": ["Could not solve the expression."],
            "answer": str(e)
        }), 400


if __name__ == "__main__":
    app.run(debug=True)
