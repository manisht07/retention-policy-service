from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# --- Operator Dispatch Maps ---

LOGICAL_OPERATORS = {
    "equals": lambda a, b: a == b,
    "not_equals": lambda a, b: a != b,
    "in": lambda a, b: a in b,
    "not_in": lambda a, b: a not in b,
    "greater_than": lambda a, b: a > b,
    "less_than": lambda a, b: a < b,
    "greater_than_or_equal": lambda a, b: a >= b,
    "less_than_or_equal": lambda a, b: a <= b,
    "is_null": lambda a, _: a is None,
    "is_not_null": lambda a, _: a is not None,
}

DATE_OPERATORS = {
    "add_days": lambda date, value: date + timedelta(days=value),
    "add_months": lambda date, value: date + relativedelta(months=value),
    "add_years": lambda date, value: date + relativedelta(years=value),
    "fixed_date": lambda _, value: datetime.strptime(value, "%Y-%m-%d"),
}

# --- Condition Evaluation ---

def evaluate_condition(condition, record):
    field = condition.get("field")
    operator = condition.get("operator")
    value = condition.get("value")
    record_value = record.get(field)

    logic_fn = LOGICAL_OPERATORS.get(operator)
    if not logic_fn:
        raise ValueError(f"Unsupported operator: {operator}")
    return logic_fn(record_value, value)

# --- Nested Logic Evaluation ---

def evaluate_logic(block, record):
    if "field" in block:  # Base condition
        return evaluate_condition(block, record)

    combinator = block["combinator"]
    conditions = block["conditions"]
    results = [evaluate_logic(cond, record) for cond in conditions]

    if combinator == "all":
        return all(results)
    elif combinator == "any":
        return any(results)
    elif combinator == "not":
        return not results[0]
    raise ValueError(f"Unsupported combinator: {combinator}")

# --- Expiration Calculation ---

def calculate_expiration(calc_block, record):
    field = calc_block["field"]
    operator = calc_block["operator"]
    value = calc_block["value"]
    base_date = datetime.strptime(record[field], "%Y-%m-%d")

    date_fn = DATE_OPERATORS.get(operator)
    if not date_fn:
        raise ValueError(f"Unsupported date operator: {operator}")
    return date_fn(base_date, value)

# --- Main Evaluation Entry Point ---

def evaluate_policy(policy: dict, record: dict) -> str:
    for rule in policy["conditions"]["rules"]:
        if "if" in rule and evaluate_logic(rule["if"], record):
            return calculate_expiration(rule["then"]["calculate"], record).strftime("%Y-%m-%d")
        elif "else" in rule:
            fallback = rule["else"]["calculate"]
    return calculate_expiration(fallback, record).strftime("%Y-%m-%d") if "fallback" in locals() else None
