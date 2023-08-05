function helpdeskGetObjectTools($) {
    var url = ADMIN_URL + "openhelpdesk/ticket/object_tools/?view=" + location.pathname;
    $.get(url, function (data) {
        var objectToolsUl = $('ul.object-tools');
        for (var key in data) {
            if ("url" in data[key] && "id" in data[key]){
                var li = '<li><a href="'+ data[key].url + '"';
                if (data[key].id) {
                    li += ' id="' + data[key].id  + '"';
                }
                objectToolsUl.append(li + '>' + data[key].text+ '</a></li>');
            }
        }
    }, "json");
}

function helpdeskInit($) {
    $("div#content-main").hide();
    $('<div id="loading"><i class="fa fa-circle-o-notch fa-spin' +
            ' fa-4x"></i> Loading...</div>').appendTo('#content');
}

function helpdeskFinalize($) {
    $("div#content-main").show();
    $("div#loading").remove();
}