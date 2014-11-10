$("#file-upload-submit").click( () ->
    data = new FormData($("#file-upload-form")[0])
    data.append("id", window.id)

    $.ajax( {
        url: "/forms/file_upload",
        type: "POST",
        data: data,
        processData: false,
        contentType: false})
)

formObject = (form) ->
    o = new Object()

    for tag in $(form).find("input")
        o[tag.name] = switch tag.type
            when "number" then Number(tag.value)
            else tag.value

    for tag in $(form).find("select")
        o[tag.name] = tag.value
    return o

$("#descriptive-stat-submit").click( () ->
    o = formObject("#descriptive-stat-form")
    o.type = "descriptive stat"
    window.socket.emit("compute", o)
)

$("#ttest_1-submit").click( () ->
    o = formObject("#ttest_1-form")
    o.type = "ttest1"
    o.mu = Number(o.mu)
    window.socket.emit("compute", o)
)
