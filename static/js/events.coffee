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

socket.on("display", (msg) ->
    $("#stat")[0].innerHTML += "<br/>" + escape(msg)
)
socket.on("data", (msg) ->
    $("#data")[0].innerHTML = msg
)
