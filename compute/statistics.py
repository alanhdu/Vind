import blaze as bz
import pandas as pd
from scipy import stats

def describe(data, column):
    data = bz.into(pd.Series, data[column])
    result = data.quantile([0, 0.25, 0.5, 0.75, 1])
    result.index = ["Min", "1st Quartile", "Median", "3rd Quartile", "Max"]

    result["IQR"] = result["3rd Quartile"] - result["1st Quartile"]
    result["Mean"] = data.mean()
    result["Std Dev"] = data.std()
    result["N"] = len(result)

    return pd.DataFrame({column: result}).T.to_html()

def ttest1(data, column, mu=0):
    data = bz.into(pd.Series, data[column])
    t, p = stats.ttest_1samp(data, mu)
    return "t = {t}, p-value = {p}".format(t=t, p=p)
