// webapp.js
// Yuelin Kuang and Lucie Wolf 
// Nov 9, 2022

// Returns the base URL of the API, onto which endpoint
// components can be appended.

window.onload = initialize;

function initialize() {
    loadGenresSelector();

    let element = document.getElementById('search_button');
    if (element) {
        element.onclick = onGamesFilterChanged;
    }
}

// Returns the base URL of the API, onto which endpoint
// components can be appended.
function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}

function loadGenresSelector() {
    let url = getAPIBaseURL() + '/genres/';

    // Send the request to the books API /genres/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(genres) {
        // Add the <option> elements to the <select> element
        let selectorBody = '<option value="None">Choose a Genre!</option>\n';
        for (let k = 0; k < genres.length; k++) {
            let genre = genres[k];
            selectorBody += '<option value="' + genre['id'] + '">' + genre['genre_name'] + '</option>\n';
        }

        let selector = document.getElementById('genre_selector');
        if (selector) {
            selector.innerHTML = selectorBody;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

function onGamesFilterChanged() {
    let url = getAPIBaseURL() + '/games/?';

    let genre_selector = document.getElementById('genre_selector');
    let genreID = genre_selector.value;

    let title_input = document.getElementById('title_search').value;

    if (genreID != 'None') {
        url += 'genre_id=' + genreID; 
    }
    
    if (title_input != '') {
        if (url.charAt(url.length - 1) == '?') {
            url += 'title=' + title_input;
        }
        else {
            url += '&title=' + title_input;
        }    
    }

    if (url.charAt(url.length - 1) == '?') {
        url.slice(0, -1);
    }

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(games) {
        let game_html = '';
        for (var i = 0; i < games.length; i++) {
            var game = games[i];
            game_html += '<div class="game_item flex" id="' + game['id'] + '">'
                        + '<img class="game_img" alt="Header Image for ' + game['title'] + '" src="' + game['media']['header_image'] + '">'
                        + '<p style="margin-left: 10px;"><strong>' + game['title'] + '</strong><br>'
                        + game['description'] + '</p>'
                        + '</p></div>\n';
        }
    
        var games_container = document.getElementById('games_container');
        if (games_container) {
            games_container.innerHTML = game_html;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}


function selectOrDeselect() {
    var inputs = document.getElementsByTagName("input");

    var selected = true;
    for(var i = 0; i < inputs.length; i++) {
        if(inputs[i].type == "checkbox") {
            if(inputs[i].checked == false) {
                selected = false;
            }
        }  
    }

    for(var i = 0; i < inputs.length; i++) {
        if(inputs[i].type == "checkbox") {
            inputs[i].checked = !selected; 
        }  
    }
}