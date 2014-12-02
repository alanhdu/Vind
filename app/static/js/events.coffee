window.hash = (obj) ->
    func = (a, b) ->
        a = ((a << 5) - a) + b.charCodeAt(0)
        return a & a
    return JSON.stringify(obj).split("").reduce(func, 0)
