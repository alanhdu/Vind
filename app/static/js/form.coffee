$("#file_upload_submit").click( () ->
    #$.post("/forms/file_upload", $("#file_upload_form").serialize())
    #console.log($("#file_upload_form").serialize())
    #
    $.ajax( {
        url: "/forms/file_upload",
        type: "POST",
        data: new FormData($("#file_upload_form")[0]),
        processData: false,
        contentType: false})
)
