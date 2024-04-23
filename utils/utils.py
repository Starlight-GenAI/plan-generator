from typing import List

def is_outlier(data,q1,q3,IQR):
    if data >= (q3 + 1.5*IQR) or data <= (q1 - 1.5*IQR):
        return True
    return False

def calculate_interquartile_range(data: List[float]):
    sorted_data = sorted(data)
    q1 = sorted_data[int(len(sorted_data)/4)]
    q3 = sorted_data[int(3*len(sorted_data)/4)]
    IQR = q3 - q1
    return (q1,q3,IQR)
    