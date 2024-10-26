class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type  # 'operator' or 'operand'
        self.left = left
        self.right = right
        self.value = value  # For operand, this could be a comparison (e.g. 'age > 30')

    def evaluate(self, data):
        if self.type == 'operand':
            return self._evaluate_operand(data)
        elif self.type == 'operator':
            return self._evaluate_operator(data)
        
    def _evaluate_operand(self, data):
        # Logic for operand evaluation, e.g., data['age'] > 30
        attribute, operator, comparison = self.value
        return eval(f"{data[attribute]} {operator} {comparison}")

    def _evaluate_operator(self, data):
        if self.value == 'AND':
            return self.left.evaluate(data) and self.right.evaluate(data)
        elif self.value == 'OR':
            return self.left.evaluate(data) or self.right.evaluate(data)

def create_rule(rule_string):
    # Code to parse a rule string and return the root Node (AST)
    pass

def combine_rules(rules):
    # Code to combine multiple rule ASTs into one, with optimizations
    pass

import re

def create_rule(rule_string):
    # Remove whitespace
    rule_string = rule_string.replace(" ", "")
    
    # Use regex to tokenize the rule string
    tokens = re.findall(r'\d+|\'[^\']*\'|[A-Za-z]+|[<>=!]+|[()&|]', rule_string)

    def parse_expression(tokens):
        token = tokens.pop(0)
        
        if token == '(':
            left = parse_expression(tokens)
            operator = tokens.pop(0)  # AND / OR
            right = parse_expression(tokens)
            tokens.pop(0)  # Remove the closing ')'
            return Node('operator', left, right, operator)
        else:
            # It's an operand
            if re.match(r'\d+', token):  # Numeric comparison
                return Node('operand', value=int(token))
            elif re.match(r'\'[^\']*\'', token):  # String comparison
                return Node('operand', value=token.strip("'"))
            else:
                # Assume the token is a variable (e.g., 'age', 'department')
                return Node('operand', value=token)

    return parse_expression(tokens)

def combine_rules(rules):
    combined_root = None
    
    for rule in rules:
        current_ast = create_rule(rule)
        
        if combined_root is None:
            combined_root = current_ast
        else:
            # Combine the current AST with the existing one using AND
            combined_root = Node('operator', combined_root, current_ast, 'AND')

    return combined_root

def evaluate_rule(ast_node, data):
    if ast_node.type == 'operand':
        # Evaluate operand nodes
        if isinstance(ast_node.value, int):
            return data[ast_node.value]  # Assuming data contains an int
        elif isinstance(ast_node.value, str):
            return data[ast_node.value]  # Assuming data contains a string
    elif ast_node.type == 'operator':
        left_eval = evaluate_rule(ast_node.left, data)
        right_eval = evaluate_rule(ast_node.right, data)
        
        if ast_node.value == 'AND':
            return left_eval and right_eval
        elif ast_node.value == 'OR':
            return left_eval or right_eval

# Example usage
# data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
# ast = create_rule("((age > 30 AND department = 'Sales'))")
# result = evaluate_rule(ast, data)

if __name__ == "__main__":
    rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    ast = create_rule(rule1)
    
    data = {
        "age": 35,
        "department": "Sales",
        "salary": 60000,
        "experience": 3
    }
    
    result = evaluate_rule(ast, data)
    print("Evaluation Result:", result)  # Should print True or False based on the rule
