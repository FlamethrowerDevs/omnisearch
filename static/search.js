function queue_chunk(chunk_id) {
    // todo: check continuously until the next chunk is ready every 100ms
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