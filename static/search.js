function search(query, config){
    console.log("Beginning search...");
    fetch("/api/search?query="+encodeURIComponent(query)+"&config="+encodeURIComponent(config))
}

const urlParams = new URLSearchParams(window.location.search);
search(urlParams.get('query'), urlParams.get('config'));
