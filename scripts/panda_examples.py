import pandas as pd

dates = pd.to_datetime(["2023-03-01", "2023-03-02", "2023-03-03"])
data = {
    "Open": [100.0, 102.5, 101.0],
    "High": [103.0, 103.5, 102.0],
    "Low": [99.5, 101.8, 100.5],
    "Close": [102.0, 102.2, 101.5],
    "Volume": [1500, 1800, 1700],
}

df = pd.DataFrame(data, index=dates)
df.index.name = "Date"

print(df)

"""
             Open   High    Low  Close  Volume
Date                                         
2023-03-01  100.0  103.0   99.5  102.0    1500
2023-03-02  102.5  103.5  101.8  102.2    1800
2023-03-03  101.0  102.0  100.5  101.5    1700
"""