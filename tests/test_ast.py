import pytest
from app.ast_engine import create_rule, evaluate_rule

def test_create_rule():
    rule = "age > 30 AND department = 'Sales'"
    ast = create_rule(rule)
    assert ast is not None

def test_evaluate_rule():
    rule = "age > 30 AND department = 'Sales'"
    ast = create_rule(rule)
    data = {"age": 35, "department": "Sales"}
    assert evaluate_rule(ast, data) == True
