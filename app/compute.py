import blaze as bz
import pandas as pd

def tukeyFiveNum(data):
    df = bz.into(pd.DataFrame, data)
    result = df.quantile([0, 0.25, 0.5, 0.75, 1])
    result.index = ["Min", "1st Quartile", "Median", "3rd Quartile", "Max"]
    return result.T

def meanStd(data):
    df = bz.into(pd.DataFrame, data)
    result = pd.DataFrame()
    result["Mean"] = df.mean()
    result["Std Dev"] = df.std()
    return result
    
