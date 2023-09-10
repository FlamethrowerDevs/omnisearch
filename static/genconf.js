function generate_config(){
    console.log(options_json);
    var config = {"searchers": [], "filters": [], "sorters": []};
    for (var i = 0; i < options_json.searchers.length; i++){
        var option = options_json.searchers[i];
        var elem = document.getElementById("advanced_"+option.id);
        if (elem.type == "checkbox" && elem.checked){
            config.searchers.push(option.name);
        }
    }
    for (var i = 0; i < options_json.filters.length; i++){
        var option = options_json.filters[i];
        var elem = document.getElementById("advanced_"+option.id);
        if (elem.type == "checkbox" && elem.checked){
            config.filters.push(option.name);
        }
    }
    for (var i = 0; i < options_json.sorters.length; i++){
        var option = options_json.sorters[i];
        var elem = document.getElementById("advanced_"+option.id);
        if (elem.type == "checkbox" && elem.checked){
            config.sorters.push(option.name);
        }
    }
    // set config hidden input
    document.getElementById("configinput").value = JSON.stringify(config);

    return true;
}

// Path: static/search.js