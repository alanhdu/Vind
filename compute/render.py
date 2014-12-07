from decorator import decorator

def wrap_results(f):
    return decorator(_results, f)

def _results(func, *args, **kwargs):
    return Results(results=func(*args, **kwargs))

class Results(object):
    assumptions, results = None, None

    def __init__(self, assumptions=None, results=None):
        self.assumptions = [] if assumptions is None else assumptions
        self.results = [] if results is None else results

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
            f = "<p> {conf:0.2%} Confidence Interval:\({low}, {high}\) </p>"
            s += f.format(conf=conf, low=low, high=high)
        if self.Ho:
            h_name, h_value = self.Ho
            t_name, t_value = self.test
            h_value, t_value, p = format_float(h_value), format_float(t_value), format_float(self.p)
            f = "<p> For \(H_o: {h_name}={h_value} \), \({t_name}={t_value}\), \(p={p}\) </p>"
            s += f.format(h_name=h_name, h_value=h_value, t_name=t_name, 
                          t_value=t_value, p=p)
        return s
