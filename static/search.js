function search(query, config){
    console.log("Beginning search...");
    fetch("/api/search?query="+encodeURIComponent(query)+"&config="+encodeURIComponent(config)).then(function(response){
        console.log("Got response, parsing and displaying...");
        response.json().then(function(data){
            console.log("Got results:", data);
            html = "<ul>";
            for (var i = 0; i < data.length; i++){
                html += "<li><a href='"+data[i]+"'>"+data[i]+"</a></li>";
            }
            html += "</ul>";
            document.getElementById("resultdiv").remove();
            document.getElementById("results").innerHTML = html;
        });
    });
}

const urlParams = new URLSearchParams(window.location.search);
search(urlParams.get('query'), urlParams.get('config'));