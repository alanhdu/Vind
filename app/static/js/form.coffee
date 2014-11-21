$("#file-upload-submit").click( () ->
    data = new FormData($("#file-upload-form")[0])
    data.append("id", window.id)

    $.ajax({
        url: "/forms/file_upload",
        type: "POST",
        data: data,
        processData: false,
        contentType: false})
)

formObject = (form) ->
    o = {
        "parameters": new Object()
        "data": new Object()
    }
    for tag in $(form).find("input")
        value = switch tag.type
            when "number" then Number(tag.value)
            else tag.value

        if "parameter" in tag.classList
            o["parameters"][tag.name] = value
        if "data" in tag.classList
            o["data"][tag.name] = value

    for tag in $(form).find("select")
        if "parameter" in tag.classList
            o["parameters"][tag.name] = tag.value
        if "data" in tag.classList
            o["data"][tag.name] = tag.value
    return o

registerForm = (id, title) ->
    $("#" + id + "-submit").click(() ->
        o = formObject("#" + id + "-form")
        o.type = title
        window.compute(o)
    )

registerForm("descriptive-stat", "descriptive stat")
registerForm("ttest1", "ttest1")
