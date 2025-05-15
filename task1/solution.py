def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        params = kwargs.copy()
        idx = 0
        for k, _ in annotations.items():
            if k == "return":
                continue
            if k not in params:
                params[k] = args[idx]
                idx += 1
        for kwarg in params:
            expected_type = annotations[kwarg]
            value = params[kwarg]
            if type(value) is not expected_type:
                raise TypeError(
                    f"Аргумент {kwarg}={params[kwarg]} имеет тип {type(params[kwarg]).__name__} вместо ожидаемого {annotations[kwarg].__name__}"
                )

        result = func(*args, **kwargs)
        if "return" in annotations:
            expected_type = annotations["return"]
            if type(result) is not expected_type:
                raise TypeError(
                    f"Результат выполнения функции {result} имеет тип {type(result).__name__} вместо ожидаемого {annotations["return"].__name__}"
                )
        return result

    return wrapper


if __name__ == "__main__":

    @strict
    def sum_two(a: int, b: int) -> int:
        return a + b

    print(sum_two(1, 2))
