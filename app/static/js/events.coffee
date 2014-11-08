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
window.socket = socket

socket.on("connect", () -> socket.emit("begin", {}))

socket.on("register", (msg) ->
    window.id = msg["id"]
)

for tag in $(".display")
    tag.scrollTop = tag.scrollHeight

socket.on("display", (msg) ->
    tag = $("#result")[0]
    if msg["type"] == "stat"
        if msg["safe"]
            tag.innerHTML += msg["display"] + "<br/>"
        else
            tag.innerHTML += escape(msg["display"]) + "<br/>"
    else if msg["type"] == "graph"
        script = $(msg["display"])[0]   # get script DOM
        tag.appendChild(script)
        $.getScript(script.src)
    tag.scrollTop = tag.scrollHeight    # scroll to bottom
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
)
