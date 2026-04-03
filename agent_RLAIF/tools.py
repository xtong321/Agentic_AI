"""
simple tools
"""

import math

def calculator(expression: str):
    try:
        return str(eval(expression))
    except:
        return "Error in calculation"

def search_tool(query: str):
    # simplified version: be able to use API later
    fake_db = {
        "EV companies": "Tesla, BYD, Rivian",
        "Tesla revenue": "Tesla revenue is about $96B (2023)",
        "BYD revenue": "BYD revenue is about $85B",
    }
    return fake_db.get(query, "No result found")