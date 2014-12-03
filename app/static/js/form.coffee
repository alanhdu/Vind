send = (url, data, success) ->
    $.ajax({
        url: url, type: "POST", data: data,
        processData: false, contentType: false}).done(success)

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
    send("/forms/file_upload", data, success)
)


class Analysis
    constructor: (@type, @title) ->
        @parameters = {}
        @data = {}

        form = $("##{@type}-form")

        for tag in form.find("input")
            if tag.type == "number"
                value = Number(tag.value)
            else
                value = tag.value

            if "parameter" in tag.classList
                @parameters[tag.name] = value
            if "data" in tag.classList
                @data[tag.name] = value

        for tag in form.find("select")
            if "parameter" in tag.classList
                @parameters[tag.name] = tag.value
            if "data" in tag.classList
                @data[tag.name] = tag.value

        @hash = window.hash(@data) + window.hash(@type)

    to_json: () ->
        return JSON.stringify({data: @data, type: @type, parameters:@parameters})
    compute: (panel) ->
        type = @type
        render = (result) ->
            titleTag = panel.find(".analysis-title")[0]
            contentTag = panel.find(".analysis")[0]
            contentTag.innerHTML = JSON.parse(result).result
            titleTag.innerHTML = type
            MathJax.Hub.Typeset(contentTag) # technically should be async
        send("/forms/statistics", @.to_json(), render)


class AnalysisCollection
    constructor: () ->
        @analyses = {}
        @panels = {}

    add: (id, title) ->
        g = new Analysis(id, title)
        if g.hash of @analyses
            # if nothing's changed, to bother recomputing
            if JSON.stringify(g) != JSON.stringify(@analyses[g.hash])
                @analyses[g.hash].parameters = g.parameters
                @analyses[g.hash].compute(@panels[g.hash])
        else
            @analyses[g.hash] = g
            panel = $("""
            <div class="panel panel-default">
               <div class="panel-heading" role="tab">
                   <h4 class="panel-title"> 
                       <a id="#{g.hash}_title" class="analysis-title" data-toggle="collapse" href="##{g.hash}"> #{g.type} </a> 
                   </h4>
               </div>
               <div id="#{g.hash}" class="analysis panel-collapse collapse in result-panel" role="tabpanel"></div>
            </div>""")

            tag = $("#results").append(panel)
            @panels[g.hash] = panel
            tag.append(g.panel)
            g.compute(@panels[g.hash])
        return null

            
window.analyses = new AnalysisCollection()

registerForm = (id, title) ->
    $("##{id}-submit").click(() ->
        window.analyses.add(id, title)
    )

registerForm("descriptive-stat", "Descriptive Statistics")
registerForm("ttest1", "1 Sample T-Test")
