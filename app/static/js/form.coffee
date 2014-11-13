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

registerForm = (id, title) ->
    $("#" + id + "-submit").click(() ->
        o = formObject("#" + id + "-form")
        o.type = title
        window.compute(o)
    )

registerForm("descriptive-stat", "descriptive stat")
registerForm("ttest_1", "ttest1")
