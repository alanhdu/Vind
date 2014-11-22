escape = (str) ->
    String(str).replace(/[& <>"\n]/g, (chr) ->
        switch chr
            when '\n' then "<br/>"
            when ' ' then "&nbsp;"
            when '>' then "&gt;"
            when '<' then "&lt;"
            when '"' then "&quot;"
            when '&' then "&amp;"
    )

socket = io.connect()
socket.on("connect", () -> socket.emit("begin", {}))
socket.on("register", (msg) ->
    window.id = msg["id"]
)

window.hash = (obj) ->
    func = (a, b) ->
        a = ((a << 5) - a) + b.charCodeAt(0)
        return a & a
    return JSON.stringify(obj).split("").reduce(func, 0)

window.compute = (obj) ->
    socket.emit("compute", obj)

socket.on("result", (msg) ->
    tag = $("#results")[0]
    id = window.hash(msg["description"]["data"])

    titleTag = $("#" + id + "_title")[0]
    contentTag = $("#" + id)[0]
    if msg["type"] == "stat"
        if msg["safe"]
            contentTag.innerHTML = msg["display"]
        else
            contentTag.innerHTML = escape(msg["display"])
        titleTag.innerHTML = msg["description"]["type"]
        MathJax.Hub.Typeset(contentTag) # technically should be async
    else if msg["type"] == "graph"
        script = $(msg["display"])[0]   # get script DOM
        newTag.appendChild(script)
        $.getScript(script.src)

    tag.scrollTop = tag.scrollHeight    # scroll to bottom

    $("#" + id).data(msg["description"])
)

socket.on("data", (msg) ->
    $("#data")[0].innerHTML = msg
    for select in $(".column-select")
        select.innerHTML = ""
        for tag in $("#data").find("thead").find("th")
            if tag.textContent
                option = document.createElement("option")
                option.innerHTML = tag.textContent
                option.value = tag.textContent
                select.appendChild(option)
    #for tag in $(".result-panel")
)
