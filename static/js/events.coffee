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

for tag in $(".meaningful")
    s = tag.text.trim().toLowerCase()   # corresponding socketio name
    tag.onclick = () -> socket.emit(s, {})

for tag in $(".display")
    tag.scrollTop = tag.scrollHeight

socket.on("display", (msg) ->
    tag = $("#result")[0]
    if msg["safe"]
        tag.innerHTML += "<br/>" + msg["display"]
    else
        tag.innerHTML += "<br/>" + escape(msg["display"])
    tag.scrollTop = tag.scrollHeight    # scroll to bottom
)

socket.on("data", (msg) ->
    $("#data")[0].innerHTML = msg
)
