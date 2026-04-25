from data import SeriesDataLoader

class Transformation:
    def __init__(self, series_file_path):
        self.db_client = SeriesDataLoader(series_file_path)

    def apply_transformation(self, transformation_name, *args):
        transfomation_map = {
            "Fetch": self.fetch,
            "SimpleMovingAverage": Transformation.simple_moving_average,
            "ExponentialMovingAverage": Transformation.exponential_moving_average,
            "RateOfChange": Transformation.rate_of_change,
            "CrossAbove": Transformation.cross_above,
            "ConstantSeries": Transformation.constant_series,
            "PortfolioSimulation": Transformation.portfolio_simulation
        }
        transformation = transfomation_map[transformation_name]
        return transformation(*args)
    
    def fetch(self, data_source: str):
        return self.db_client.get_series(data_source)
    
    @staticmethod
    def simple_moving_average(window: int, A: list[float | int]) -> list[float]:
        n = len(A)
        B = [None] * (window - 1)
        windows_sum = sum(A[:window])
        for t in range(window - 1, n):
            B.append(windows_sum/window)
            if t + 1 < n:
                windows_sum -= A[t - window + 1]
                windows_sum += A[t+1]
        return B


    @staticmethod
    def exponential_moving_average(alpha: float, A: list[float | int]) -> list[float]:
        n = len(A)
        B = [A[0]]
        for t in range(1, n):
            B.append(alpha * A[t] + (1 - alpha) * B[t - 1])
        return B


    @staticmethod
    def rate_of_change(period: int, A: list[float | int]) -> list[float]:
        period = int(period)
        n = len(A)
        B = [None] * n
        for t in range(n):
            if t - period < 0 or A[t - period] == 0:
                continue
            B[t] = (A[t] - A[t - period]) / A[t-period]
        return B

    @staticmethod
    def cross_above(A1: list[float], A2: list[float | int]) -> list[int]:
        n1 = len(A1)
        n2 = len(A2)
        B = [0] * max(n1, n2)
        for t in range(1, min(n1, n2)):
            valid = None not in [A1[t - 1], A1[t], A2[t-1], A2[t]]
            B[t] = int(valid and A1[t - 1] < A2[t - 1] and A1[t] > A2[t])
        return B

    @staticmethod
    def constant_series(k: float, A: list[float | int]) -> list[float]:
        return [k] * len(A)

    #TODO: 0 or 1 in type hint
    @staticmethod
    def portfolio_simulation(balance: float, price: list[float], entry: list[int], exit: list[int]) -> list[float]:
        n = len(price)
        positions_held = 0
        portfolio = [0.0] * n
        for i in range(n):
            if exit[i] == 1:
                balance += positions_held * price[i]
            elif entry[i] == 1:
                positions_held += 1
                balance -= price[i]
            portfolio[i] = balance + positions_held * price[i]
        return portfolio



