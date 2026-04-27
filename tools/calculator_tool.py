def calculate(expression):
    # Выполнение математического выражения, переданного в виде строки.
    try:
        result = eval(expression)
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }