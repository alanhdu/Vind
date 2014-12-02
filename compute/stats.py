import numpy as np
import blaze as bz
import pandas as pd
from scipy import stats

def describe(df, data, parameters):
    column = data["column"]


    df = bz.into(pd.Series, df[column])
    result = df.quantile([0, 0.25, 0.5, 0.75, 1])
    result.index = ["Min", "1st Quartile", "Median", "3rd Quartile", "Max"]

    result["IQR"] = result["3rd Quartile"] - result["1st Quartile"]
    result["Mean"] = df.mean()
    result["Std Dev"] = df.std()
    result["N"] = len(df)

    return pd.DataFrame({column: result}).T.to_html()

def ttest1(df, data, parameters):
    mu = parameters["mu"]
    column = data["column"]

    df = bz.into(pd.Series, df[column]).dropna()

    n = len(df)
    crit_val = stats.t.ppf(0.5 + 0.5*0.95, n-1)  # 95% CI
    std_err = df.std() / np.sqrt(n)
    mean = df.mean()
    confidence_interval = mean - crit_val * std_err, mean + crit_val * std_err 

    s = "95% CI: {}".format(confidence_interval)

    if mu is not None:
        t, p = stats.ttest_1samp(df, mu)
        return s + "<br/>" + "For \(H_0: \mu={mu}\): \(t={t}\), \(p={p}\)".format(mu=mu, t=t, p=p)
    return s
