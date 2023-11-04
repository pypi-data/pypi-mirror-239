from math import radians, cos, sin, asin, sqrt
from typing import List


def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance between two points on the
    earth (specified in decimal degrees), returns the distance in
    kilometers.
    All arguments must be of equal length.
    :param lon1: longitude of first place
    :param lat1: latitude of first place
    :param lon2: longitude of second place
    :param lat2: latitude of second place
    :return: distance in kilometers between the two sets of coordinates
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r


def calculate_error(predicted: List, real_values: List):
    """
    Calculate the error between the predicted values and the real values
    :param predicted: list of predicted values
    :param real_values: list of real values
    :return: error
    """
    error = 0
    real_sum = sum(real_values)
    for i in range(len(predicted)):
        error += abs(predicted[i] - real_values[i])
    return error / real_sum


def get_clientes_importantes():
    return [
        10001,
        10002,
        10003,
        10004,
        10005,
        10006,
        10007,
        10008,
        10009,
        10011,
        10012,
        10013,
    ]


def get_productos_importantes():
    return [20001, 20002, 20003, 20004, 20005, 20006, 20007, 20009, 20011, 20032]
