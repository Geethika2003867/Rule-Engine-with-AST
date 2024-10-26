from flask import Flask, request, jsonify
from app.ast_engine import create_rule, combine_rules, evaluate_rule

app = Flask(__name__)

@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    rule_string = request.json['rule']
    rule_ast = create_rule(rule_string)
    return jsonify({"message": "Rule created", "ast": str(rule_ast)})

@app.route('/evaluate', methods=['POST'])
def evaluate_rule_api():
    rule_ast = request.json['ast']
    data = request.json['data']
    result = evaluate_rule(rule_ast, data)
    return jsonify({"eligible": result})

if __name__ == "__main__":
    app.run(debug=True)
