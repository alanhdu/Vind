import pandas as pd
import blaze as bz

from bokeh import plotting

def scatter(data, x="SepalLength", y="SepalWidth"):
    plotting.figure()
    plotting.hold()
    df = bz.into(pd.DataFrame, data[[x, y]])
    plotting.circle(df[x], df[y])

    return plotting.curplot(), plotting.cursession()
