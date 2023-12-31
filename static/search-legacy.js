function search(query, config){
    console.log("Beginning search...");
    // start timer for display
    var time = performance.now();
    fetch("/api/search?query="+encodeURIComponent(query)+"&config="+encodeURIComponent(config)).then(function(response){
        console.log("Got response, parsing and displaying...");
        response.json().then(function(data){
            console.log("Got results:", data);
            // display time
            var html = "";
            time = performance.now() - time;
            if (data.length != 0) {
                html = "<ul>";
                for (var i = 0; i < data.length; i++){
                    html += "<li><a href='"+data[i]+"'>"+data[i]+"</a></li>";
                }
                html += "</ul><br><p>Search took "+time+"ms</p>";
            } else {
                html = "<p>No results found. How is that even possible?</p>"
            }
            document.getElementById("resultdiv").remove();
            document.getElementById("results").innerHTML = html;
        });
    });
}

const urlParams = new URLSearchParams(window.location.search);
search(urlParams.get('query'), urlParams.get('config'));