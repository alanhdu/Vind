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
