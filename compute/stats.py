import numpy as np
import blaze as bz
import pandas as pd
from scipy import stats
from .render import Results, wrap_results, StatisticalTest

@wrap_results
def describe(df, data, parameters):
    column = data["column"]     # INPUT

    df = bz.into(pd.Series, df[column])
    description = df.quantile([0, 0.25, 0.5, 0.75, 1])
    description.index = ["Min", "1st Quartile", "Median", "3rd Quartile", "Max"]

    description["IQR"] = description["3rd Quartile"] - description["1st Quartile"]
    description["Mean"] = df.mean()
    description["Std Dev"] = df.std()
    description["N"] = len(df)

    description = pd.DataFrame({"description":description}).T   # OUTPUT
    return [description]

@wrap_results
def ttest1(df, data, parameters):
    mu_0 = parameters["mu"]       # INPUT
    column = data["column"]     # INPUT
    conf = parameters.get("conf", 0.95) # INPUT

    df = bz.into(pd.Series, df[column]).dropna()

    n = len(df)
    crit_val = stats.t.ppf(0.5 + 0.5*conf, n-1)
    std_err = df.std() / np.sqrt(n)
    mean = df.mean()            # OUTPUT
    ci = mean - crit_val * std_err, mean + crit_val * std_err  # OUTPUT

    s = StatisticalTest(ci=(conf, ci), stat=("\mu", mean))

    if mu_0 is not None:
        t, p = stats.ttest_1samp(df, mu_0)  # OUTPUT
        s.Ho = ("\mu_0", mu_0)
        s.test = ("t", t)
        s.p = p
    return [s]
