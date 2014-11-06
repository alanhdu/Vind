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

for tag in $(".stat")
    s = tag.text.trim().toLowerCase()   # corresponding socketio name
    # do (s) -> -> for weird function closure thing w/ JS
    tag.onclick = do (s) -> -> socket.emit("stat", s)

for tag in $(".graph")
    s = tag.text.trim().toLowerCase()
    tag.onclick = do (s) -> -> socket.emit("graph", s)

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
    alert("Receiving")
    $("#data")[0].innerHTML = msg
)
