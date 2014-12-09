import inspect

import blaze as bz
import pandas as pd
from scipy import stats
import numpy as np

from IPython.nbformat import current
from decorator import decorator

def wrap_results(f):
    d = decorator(_results, f)
    if hasattr(f, "__wrapped__"):
        d.__wrapped__ = f.__wrapped__
    return d

def _results(func, *args, **kwargs):
    return Results(func, *args, **kwargs)

class Results(object):
    assumptions, results, code, data, parameters = None, None, None, None, None

    def __init__(self, func, df, data, parameters):
        self.results = func(df, data, parameters)
        self.code = inspect.getsource(func)
        self.data = data
        self.parameters = parameters
        self.assumptions = []

    def to_ipython_cell(self, df):
        code = []
        outputs = []
        local = {"data": self.data, "parameters": self.parameters}
        for line in self.code.split("\n"):
            if line.endswith("# INPUT"):
                a, b = line.split("=")
                a, b = a.strip(), b.strip()
                value = eval(b, None, local)
                line = '{a} = {value}'.format(a=a, value=repr(value))
                code.append(line)
            elif line.endswith("# OUTPUT"):
                a, b = line.split("=")
                outputs += [x.strip() for x in a.split(",")]

                code.append(line[4:-len("# OUTPUT")].rstrip())

            elif "def" not in line and not line.startswith("@") and "return" not in line:
                code.append(line[4:])   # get rid of first indent

        code = "\n".join(code)
        gs = {"bz": bz, "pd": pd, "df": df, "stats": stats, "np":np, "StatisticalTest":StatisticalTest}
        ls = {}
        exec(code, gs, ls)

        output_cells = []
        for output in outputs:
            kwargs = {}
            if hasattr(ls[output], "to_html"):
                kwargs["output_html"] = ls[output].to_html()

            o = current.new_output("display_data", str(ls[output]), **kwargs)
            output_cells.append(o)

            code += "\ndisplay({})".format(output)

        return current.new_code_cell(code, outputs=output_cells)


    def to_html(self):
        s = "<h4> Assumptions: </h4>"
        s += "<div>" + "".join(a.to_html() for a in self.assumptions) + "</div>"
        s += "<h4> Results: </h4>"
        s += "<div>" + "".join(r.to_html() for r in self.results) +  "</div>"

        return s

def format_float(f):
    s = "{:.4e}".format(f)
    number, exp =  s.split("e")
    number, exp = float(number), int(exp)

    return "{number} \\times 10^{{ {exp} }}".format(number=number, exp=exp)
    

class StatisticalTest(object):
    ci, Ho, p, stat, test = None, None, None, None, None

    def __init__(self, ci=None, Ho=None, p=None, stat=None, test=None):
        self.ci = ci
        self.Ho = Ho
        self.p = p
        self.test = test
        self.stat = stat

    def to_html(self):
        s = ""
        if self.stat:
            name, stat = self.stat
            stat = format_float(stat)
            s += "<p> \({name} = {stat}\) </br> </p>".format(name=name, stat=stat)
        if self.ci:
            conf, (low, high) = self.ci
            low, high = format_float(low), format_float(high)
            f = "<p> {conf:0.2%} Confidence Interval: \({low}, {high}\) </p>"
            s += f.format(conf=conf, low=low, high=high)
        if self.Ho:
            h_name, h_value = self.Ho
            t_name, t_value = self.test
            h_value, t_value, p = format_float(h_value), format_float(t_value), format_float(self.p)
            f = "<p> For \(H_0: {h_name}={h_value} \), \({t_name}={t_value}\), \(p={p}\) </p>"
            s += f.format(h_name=h_name, h_value=h_value, t_name=t_name, 
                          t_value=t_value, p=p)
        return s
