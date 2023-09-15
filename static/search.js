function queue_chunk(chunk_id) {
    console.log("Queueing chunk:", chunk_id);
    if (chunk_id == "-1") {
        return; // end of results
    }

    function interval_func() {
        fetch("/api/get_chunk/"+chunk_id).then(function(response){
            response.json().then(function(data){
                console.log("Got chunk:", data);
                if (data.error && data.error != "Chunk not ready") {
                    console.log("Error:", data.error);
                    clearInterval(interval);
                    return;
                }
                else {
                    clearInterval(interval);
                    handle_data(data);
                }
            });
        });
    }
    
    var interval = setInterval(interval_func, 400);
}

function handle_initial_data(data) {
    var next_chunk_id = data[1];
    queue_chunk(next_chunk_id);
    var results = data[0];
    document.getElementById("resultdiv").innerHTML = "";
    for(var i = 0; i < results.length; i++) {
        var result = results[i];
        var result_html = "<div class='result'><h2><a href='"+result[0]+"'>"+result[2]+"</a></h2><p>"+result[3]+"</p><p>From "+result[1]+"</p></div>";
        document.getElementById("results").innerHTML += result_html;
    }
}

function handle_data(data) {
    var next_chunk_id = data[0];
    queue_chunk(next_chunk_id);
    var results = data[2][0];
    document.getElementById("resultdiv").innerHTML = "";
    for(var i = 0; i < results.length; i++) {
        var result = results[i];
        var result_html = "<div class='result'><h2><a href='"+result[0]+"'>"+result[2]+"</a></h2><p>"+result[3]+"</p><p>From "+result[1]+"</p></div>";
        document.getElementById("results").innerHTML += result_html;
    }
}

function search(query, config){
    console.log("Beginning search...");
    // start timer for display
    var time = performance.now();
    fetch("/api/enhanced_search?query="+encodeURIComponent(query)+"&config="+encodeURIComponent(config)).then(function(response){
        response.json().then(function(data){
            console.log("Got results:", data);
            handle_initial_data(data, time);
        });
    });
}

const urlParams = new URLSearchParams(window.location.search);
search(urlParams.get('query'), urlParams.get('config'));