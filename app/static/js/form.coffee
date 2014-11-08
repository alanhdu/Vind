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
    for field in form.serializeArray()
        o[field["name"]] = field["value"]
    return o

$("#descriptive-stat-submit").click( () ->
    o = formObject($("#descriptive-stat-form"))
    o.type = "descriptive stat"
    window.socket.emit("compute", o)
)
