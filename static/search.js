function handle_initial_data(data) {
    
}

function search(query, config){
    console.log("Beginning search...");
    // start timer for display
    var time = performance.now();
    fetch("/api/enhanced_search?query="+encodeURIComponent(query)+"&config="+encodeURIComponent(config)).then(function(response){
        response.json().then(function(data){
            console.log("Got results:", data);
            handle_initial_data(data);
        });
    });
}

const urlParams = new URLSearchParams(window.location.search);
search(urlParams.get('query'), urlParams.get('config'));