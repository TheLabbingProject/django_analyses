class Addition:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def calculate(self) -> dict:
        return {"result": sum(self.kwargs.values())}


class Power:
    def __init__(self, base: float, exponent: float):
        self.base = base
        self.exponent = exponent

    def run(self) -> dict:
        return {"result": self.base ** self.exponent}


class Division:
    def __init__(self, dividend: float, divisor: float = 2.0):
        self.dividend = dividend
        self.divisor = divisor

    def run(self) -> dict:
        return DivisionResults({"result": self.dividend / self.divisor})


class DivisionResults:
    def __init__(self, results: dict):
        self.results = results

