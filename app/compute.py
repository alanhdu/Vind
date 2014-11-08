import blaze as bz
import pandas as pd

def describe(data, column):
    data = bz.into(pd.Series, data[column])
    result = data.quantile([0, 0.25, 0.5, 0.75, 1])
    result.index = ["Min", "1st Quartile", "Median", "3rd Quartile", "Max"]

    result["IQR"] = result["3rd Quartile"] - result["1st Quartile"]
    result["Mean"] = data.mean()
    result["Std Dev"] = data.std()

    return pd.DataFrame({column: result}).T
