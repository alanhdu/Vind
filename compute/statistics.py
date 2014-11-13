import numpy as np
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

def ttest1(data, column, mu=None):
    data = bz.into(pd.Series, data[column]).dropna()

    n = len(data)
    crit_val = stats.t.ppf(0.5 + 0.5*0.95, n-1)  # 95% CI
    std_err = data.std() / np.sqrt(n)
    mean = data.mean()
    confidence_interval = mean - crit_val * std_err, mean + crit_val * std_err 

    s = "95% CI: {}".format(confidence_interval)

    if mu is not None:
        t, p = stats.ttest_1samp(data, mu)
        return s + "<br/>" + "For \(\mu_0$={mu}\): t = {t}, p = {p}".format(mu=mu, t=t, p=p)
    return s
