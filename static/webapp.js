// webapp.js
// Yuelin Kuang and Lucie Wolf 
// Nov 9, 2022

window.onload = initialize;

function initialize() {
    loadAuthorsSelector();

    let element = document.getElementById('author_selector');
    if (element) {
        element.onchange = onAuthorsSelectionChanged;
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

function loadGames() {
    let url = getAPIBaseURL() + '/games/';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(games) {
        var gameList = '';
        for (var k = 0; k < games.length; k++) {
            var game = games[k];
             gameList += '<div class="game_item flex">' 
                      + '<img class="game_img" src=' + game['links_to_images']['header_image']
                      + '> <p style="margin-left: 10px;">' + game['title <br>']
                      + game['description'] + '</p>'
                      + '</div>\n';
        }

        var games_container = document.getElementById('games_container');
        if (games_container) {
            games_container.innerHTML = gameList;
        }
    })
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