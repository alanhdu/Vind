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
    o = new Object()
    o.parameters = new Object()
    o.data = new Object()

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

getPanel = (id) ->
    """
    <div class="panel panel-default">
        <div class="panel-heading" role="tab">
            <h4 class="panel-title"> 
                <a id="#{id}_title" data-toggle="collapse" href="##{id}"></a> 
            </h4>
        </div>
        <div id="#{id}" class="panel-collapse collapse in result-panel" role="tabpanel"></div>
    </div>"""

registerForm = (id, title) ->
    $("#" + id + "-submit").click(() ->
        o = formObject("#" + id + "-form")
        o.type = title

        tag = $("#results")[0]
        rid = window.hash(o["data"])
        if $("#" +  rid).length == 0
            tag.appendChild($(getPanel(rid))[0])
        if JSON.stringify($("#" + rid).data()) != JSON.stringify(o)
            window.compute(o)
    )

registerForm("descriptive-stat", "Descriptive Statistics")
registerForm("ttest1", "1 Sample T-Test")
