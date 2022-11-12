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
            game_id = game['id']
            game_html += `
            <button class="game_item text_align_left" id="${game_id}" value="${game_id}" onclick="onGameSelected(${game_id})">
                <div class="flex">
                    <img class="game_img" alt="Header Image for ${game['title']}" src="${game['media']['header_image']}">
                    <p style="margin-left: 10px;"><strong>${game['title']}</strong><br>${game['description']}</p>
                </div>
            </button>`;
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

function onGameSelected(game_id) {
    let url = getAPIBaseURL() + '/games/specific/' + game_id; 
    
    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(game) {
        for (trait in game){
            let value = String(game[trait]);
            if (value == 'true') {
                game[trait] = '√'
            } else if (value == 'false') {
                game[trait] = 'X'
            }
        }

        if (game['minimum_age'] == 0) {
            game['minimum_age'] = '0 or unlisted';
        }

        let game_html = `
        <button class="game_item text_align_left" id="${game_id}" value="${game_id}" onclick="onGameDeselected(${game_id})">
            <div class="flex">
                <img class="game_img" alt="Header Image for ${game['title']}" src="${game['media']['header_image']}">
                <p style="margin-left: 10px;"><strong>${game['title']}</strong><br>${game['description']}</p>
            </div>
            <div class="flex">
                <div style="flex: 4"> 
                    <ul>
                        <li>Developer: ${game['developers']} </li>
                        <li>Publisher: ${game['publishers']} </li>
                        <br>
                        <li>Genres: ${game['genres']} </li>
                        <li>Categories: ${game['categories']} </li>
                        <br>
                        <li>Positive Ratings: ${game['pos_ratings']} </li>
                        <li>Negative Ratings: ${game['neg_ratings']} </li>
                        <li>Percentage of Ratings as Positive: ${Math.round(game['pos_ratings'] * 100 / (game['neg_ratings'] + game['pos_ratings']))}%</li>
                        <br>
                        <li>Price: $${game['price']} </li>
                        <li>Released on: ${game['release_date']} </li>
                        <li>Minimum age: ${game['minimum_age']} </li>
                        <li>English support: ${game['english_support']} </li>
                    </ul>
                    <table>
                        <tr><th></th><th>Windows</th><th>Mac</th><th>Linux</th></tr>
                        <tr><td>Available On</td>
                            <td> ${game['windows_support']} </td>
                            <td> ${game['mac_support']} </td>
                            <td> ${game['linux_support']} </td>
                        </tr>
                    </table>
                </div>
                <div style="flex: 3">`;

        let images = game['media']['screenshots'];
        for (var i = 0; i < images.length && i < 6; i++) {
            var image = images[i];
            game_html += `<img class="game_img" src="${image}">`;
        }
        
        game_html += '</div></div></button>'

        var selected_game_button = document.getElementById(game_id);
        if (selected_game_button) {
            //outer_html = selected_game_button.outerHTML.replace('onGameSelected(this.value)', 'onGameDeselected(this.value)');
            selected_game_button.outerHTML = game_html;
            //selected_game_button.outerHTML = outer_html;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function onGameDeselected(game_id) {
    let url = getAPIBaseURL() + '/games/specific/' + game_id; 
    
    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(game) {
        let game_html = `
        <button class="game_item text_align_left" id="${game_id}" value="${game_id}" onclick="onGameSelected(${game_id})">
            <div class="flex">
                <img class="game_img" alt="Header Image for ${game['title']}" src="${game['media']['header_image']}">
                <p style="margin-left: 10px;"><strong>${game['title']}</strong><br>${game['description']}</p>
            </div>
        </button>`;
        
        var deselected_game_button = document.getElementById(game_id);
        if (deselected_game_button) {
            //outer_html = deselected_game_button.outerHTML.replace('onGameDeselected(this.value)', 'onGameSelected(this.value)');
            //deselected_game_button.innerHTML = inner_html;
            deselected_game_button.outerHTML = game_html;
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