
def safe_eval(expr: str, names: dict):
    """
    Evaluate arithmetic expression safely using AST.
    Only numeric literals, binops, unary ops, parentheses, and the name 'ans' are allowed.
    """
    node = ast.parse(expr, mode="eval")

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)
        if isinstance(n, ast.Constant):  # Python 3.8+
            if isinstance(n.value, (int, float)):
                return n.value
            raise ValueError("Only numeric constants are allowed")
        if isinstance(n, ast.Num):  # fallback
            return n.n
        if isinstance(n, ast.BinOp):
            op_type = type(n.op)
            if op_type not in ALLOWED_BINOP:
                raise ValueError(f"Operator {op_type.__name__} not allowed")
            left = _eval(n.left)
            right = _eval(n.right)
            return ALLOWED_BINOP[op_type](left, right)
        if isinstance(n, ast.UnaryOp):
            op_type = type(n.op)
            if op_type not in ALLOWED_UNARYOP:
                raise ValueError(f"Unary operator {op_type.__name__} not allowed")
            operand = _eval(n.operand)
            return ALLOWED_UNARYOP[op_type](operand)
        if isinstance(n, ast.Name):
            if n.id in names:
                val = names[n.id]
                if isinstance(val, (int, float)):
                    return val
            raise NameError(f"Unknown name: {n.id}")
        if isinstance(n, ast.Tuple):
            raise ValueError("Tuples not allowed")
        raise TypeError(f"Unsupported expression: {type(n).__name__}")

    return _eval(node)

def print_help():
    print("Calculator - supported operations: + - * / // % ** parentheses")
    print("Commands: help, history, clear, exit, quit")
    print("Use 'ans' to reference last result (example: ans * 2)")

def main():
    ans = 0
    history = []
    print("Simple calculator. Type 'help' for commands. Ctrl-D to exit.")
    try:
        while True:
            try:
                expr = input("calc> ").strip()
            except EOFError:
                print()
                break
            if not expr:
                continue
            if expr.lower() in ("exit", "quit"):
                break
            if expr.lower() == "help":
                print_help()
                continue
            if expr.lower() == "history":
                if not history:
                    print("(no history)")
                else:
                    for i, (e, r) in enumerate(history, 1):
                        print(f"{i}: {e} = {r}")
                continue
            if expr.lower() == "clear":
                history.clear()
                ans = 0[['']]
                print("Cleared history, ans reset to 0")
                continue
            try:
                result = safe_eval(expr, {"ans": ans})
                # Normalize ints when possible
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                print(result)
                history.append((expr, result))
                ans = result
            except ZeroDivisionError:
                print("Error: division by zero")
            except Exception as e:
                print(f"Error: {e}")
    except KeyboardInterrupt:
        print()
    print("Goodbye.")

if __name__ == "__main__":
    main()