// webapp.js
// Yuelin Kuang and Lucie Wolf 
// Nov 9, 2022

// Returns the base URL of the API, onto which endpoint
// components can be appended.

window.onload = initialize;

function initialize() {
    loadGamesSelector();

    // let element = document.getElementById('author_selector');
    // if (element) {
    //     element.onchange = onAuthorsSelectionChanged;
    // }
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

function loadGamesSelector() {
    let element = document.getElementById('game_selector');
    if (!element) {
        return;
    }
    let gameID = element.value; 

    let url = getAPIBaseURL() + '/games/games/id/' + gameID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(games) {
        // Add the <option> elements to the <select> element
        let selectorBody = '';
        for (let k = 0; k < games.length; k++) {
            let game = games[k];
            selectorBody += '<option value="' + game['id'] + '">'
                                + game['title']
                                + '</option>\n';
        }

        let selector = document.getElementById('game_selector');
        if (selector) {
            selector.innerHTML = selectorBody;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

function onIdSelectionChanged() {
    let element = document.getElementById('game_selector');
    if (!element) {
        return;
    }
    let authorID = element.value; 

    let url = getAPIBaseURL() + '/games/games/id/' + authorID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(books) {
        let tableBody = '';
        for (var i = 0; i < parsed.length; i++) {
            var game = parsed[i];
            gameList += '<div class="game_item flex">' 
                        + '<img class="game_img" src=\'{{game[\'links_to_images\'][\'header_image\']}}\''
                        + '> <p style="margin-left: 10px;"> jkhj'// + game['title <br>']
                        //+ game['description'] + '</p>'
                        + '</p></div>\n';
        }
    
        var games_container = document.getElementById('games_container');
        if (games_container) {
            games_container.innerHTML = gameList;
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