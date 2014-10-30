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

for tag in $(".stat")
    s = tag.text.trim().toLowerCase()   # corresponding socketio name
    tag.onclick = do (cls, s) -> -> socket.emit("stat", s)

for tag in $(".graph")
    s = tag.text.trim().toLowerCase()   # corresponding socketio name
    tag.onclick = do (cls, s) -> -> socket.emit("stat", s)

for tag in $(".display")
    tag.scrollTop = tag.scrollHeight

socket.on("display", (msg) ->
    tag = $("#result")[0]
    if msg["safe"]
        tag.innerHTML += msg["display"] + "<br/>"
    else
        tag.innerHTML += escape(msg["display"]) + "<br/>"
    tag.scrollTop = tag.scrollHeight    # scroll to bottom
)

socket.on("data", (msg) ->
    $("#data")[0].innerHTML = msg
)
