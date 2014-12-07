send = (url, data, success) ->
    $.ajax({
        url: url, type: "POST", data: data,
        processData: false, contentType: false
    }).done(success)

$("#file-upload-submit").click( () ->
    data = new FormData($("#file-upload-form")[0])
    success = (msg) ->
        $("#data")[0].innerHTML = msg
        for select in $(".column-select")
            select.innerHTML = ""
            for tag in $("#data").find("thead").find("th")
                if tag.textContent
                    option = document.createElement("option")
                    option.innerHTML = tag.textContent
                    option.value = tag.textContent
                    select.appendChild(option)
    if $("#file-upload_data")[0].value
        send("/forms/file_upload", data, success)
    else
        alert("Form not valid")

)


class Analysis
    constructor: (@type, @title) ->
        @parameters = {}
        @data = {}

        form = $("##{@type}-form")
        for tag in form.find(":input")
            if tag.type == "number"
                value = Number(tag.value)
            else
                value = tag.value

            if "parameter" in tag.classList
                @parameters[tag.name] = value
            if "data" in tag.classList
                @data[tag.name] = value

        @id = JSON.stringify({data: @data, type: @type})

    to_json: () ->
        return JSON.stringify({data: @data, type: @type, parameters:@parameters})
    validate: () ->
        for name, value of @data
            if not value
                return false
        for name, value of @parameters
            if not value
                return false
        return true


    compute: (panel) ->
        title = @title
        render = (result) ->
            titleTag = panel.find(".analysis-title")[0]
            contentTag = panel.find(".analysis")[0]
            contentTag.innerHTML = JSON.parse(result).result
            titleTag.innerHTML = title
            MathJax.Hub.Typeset(contentTag) # technically should be async
        send("/forms/statistics", @.to_json(), render)


class AnalysisCollection
    constructor: () ->
        @analyses = {}
        @panels = {}
        @size = 0

    add: (id, title) ->
        g = new Analysis(id, title)
        if g.validate()
            if g.id of @analyses
                # if nothing's changed, don't bother recomputing
                if JSON.stringify(g) != JSON.stringify(@analyses[g.id])
                    @analyses[g.id].parameters = g.parameters
                    @analyses[g.id].compute(@panels[g.id])
            else
                @analyses[g.id] = g
                panel = $("""
                <div class="panel panel-default">
                   <div class="panel-heading" role="tab">
                       <h4 class="panel-title"> 
                           <a class="analysis-title" data-toggle="collapse" href="#analysis_#{@size}"> #{g.type} </a> 
                       </h4>
                   </div>
                   <div id="analysis_#{@size}" class="analysis panel-collapse collapse in result-panel" role="tabpanel"></div>
                </div>""")

                tag = $("#results").append(panel)
                @panels[g.id] = panel
                @size += 1
                g.compute(@panels[g.id])
        else
            alert("Form not valid")
        return null

            
window.analyses = new AnalysisCollection()

registerForm = (id, title) ->
    $("##{id}-submit").click(() -> window.analyses.add(id, title))

registerForm("descriptive-stat", "Descriptive Statistics")
registerForm("ttest1", "1 Sample T-Test")
