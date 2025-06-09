import os
import sys
from datetime import datetime

import pytest

# Ensure application modules are importable when tests are run directly with pytest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.services.rule_engine import (
    evaluate_logic,
    calculate_expiration,
    evaluate_policy,
)


def test_evaluate_logic_not_combinator():
    block = {
        "combinator": "not",
        "conditions": [
            {"field": "status", "operator": "equals", "value": "inactive"}
        ],
    }
    record = {"status": "active"}
    assert evaluate_logic(block, record) is True


def test_evaluate_logic_nested():
    block = {
        "combinator": "all",
        "conditions": [
            {"field": "region", "operator": "equals", "value": "EU"},
            {
                "combinator": "not",
                "conditions": [
                    {"field": "status", "operator": "equals", "value": "inactive"}
                ],
            },
        ],
    }
    record = {"region": "EU", "status": "active"}
    assert evaluate_logic(block, record) is True


def test_calculate_expiration_add_operations():
    record = {"created_at": "2024-01-31"}
    calc_block = {"field": "created_at", "operator": "add_days", "value": 10}
    assert calculate_expiration(calc_block, record) == datetime(2024, 2, 10)

    calc_block = {"field": "created_at", "operator": "add_months", "value": 1}
    assert calculate_expiration(calc_block, record) == datetime(2024, 2, 29)

    calc_block = {"field": "created_at", "operator": "add_years", "value": 1}
    assert calculate_expiration(calc_block, record) == datetime(2025, 1, 31)


def test_evaluate_policy_with_not():
    policy = {
        "conditions": {
            "type": "conditional",
            "rules": [
                {
                    "if": {
                        "combinator": "not",
                        "conditions": [
                            {"field": "status", "operator": "equals", "value": "inactive"}
                        ],
                    },
                    "then": {
                        "calculate": {
                            "field": "created_at",
                            "operator": "add_days",
                            "value": 30,
                        }
                    },
                },
                {
                    "else": {
                        "calculate": {
                            "field": "created_at",
                            "operator": "add_days",
                            "value": 365,
                        }
                    },
                },
            ]
        }
    }
    record = {"created_at": "2024-06-01", "status": "active"}
    assert evaluate_policy(policy, record) == "2024-07-01"
    record = {"created_at": "2024-06-01", "status": "inactive"}
    assert evaluate_policy(policy, record) == "2025-06-01"
