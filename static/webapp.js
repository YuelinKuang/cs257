// webapp.js
// Yuelin Kuang and Lucie Wolf 
// Nov 9, 2022

// Returns the base URL of the API, onto which endpoint
// components can be appended.

window.onload = initialize;

function initialize() {
    loadGenresSelector();
    loadDevelopersSelector();

    let games_search_button = document.getElementById('games_search_button');
    if (games_search_button) {
        games_search_button.onclick = onGamesFilterChanged;
    }

    let stats_search_button = document.getElementById('stats_search_button');
    if (stats_search_button) {
        stats_search_button.onclick = onStatsFilterChanged;
    }
}


//function from https://stackoverflow.com/questions/28828915/how-set-color-family-to-pie-chart-in-chart-js
function getColors(length) {
    let pallet = ["#0074D9", "#FF4136", "#2ECC40", "#FF851B", "#7FDBFF", "#B10DC9", "#FFDC00", "#001f3f", "#39CCCC", "#01FF70", "#85144b", "#F012BE", "#3D9970", "#111111", "#AAAAAA"];
    let colors = [];

    for (let i = 0; i < length; i++) {
        colors.push(pallet[i % (pallet.length - 1)]);
    }

    return colors;
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

function loadDevelopersSelector() {
    let url = getAPIBaseURL() + '/developers/';

    // Send the request to the books API /genres/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(developers) {
        // Add the <option> elements to the <select> element
        let selectorBody = '<option value="None">Choose a Developer!</option>\n';
        for (let k = 0; k < developers.length; k++) {
            let developer = developers[k];
            selectorBody += '<option value="' + developer['id'] + '">' + developer['developer_name'] + '</option>\n';
        }

        let developer_selector = document.getElementById('developer_selector');
        if (developer_selector) {
            developer_selector.innerHTML = selectorBody;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

function onGamesFilterChanged() {
    var loading_text_html = document.getElementById('loading_games');
    if (loading_text_html) {
        loading_text_html.style.display = 'inline';
    } else {
        return
    }

    let url = getAPIBaseURL() + '/games/?';

    let sort_by = ''
    if (document.getElementById('sort_title').checked) {
        sort_by = 'title'
    }
    else if (document.getElementById('sort_date').checked) {
        sort_by = 'date'
    }
    else if (document.getElementById('sort_price').checked) {
        sort_by = 'price'
    }
    else if (document.getElementById('sort_age').checked) {
        sort_by = 'age'
    }
    else if (document.getElementById('sort_pos_ratings').checked) {
        sort_by = 'pos_ratings'
    }
    else {
        sort_by = 'title'
    }

    if (document.getElementById('sort_asc').checked) {
        sort_by += '-asc'
    }
    else if (document.getElementById('sort_desc').checked) {
        sort_by += '-desc'
    }
    else {
        sort_by += '-asc'
    }
    url += 'sort_by=' + sort_by

    let genre_selector = document.getElementById('genre_selector');
    let genreID = genre_selector.value;
    if (genreID != 'None') {
        url += '&genre_id=' + genreID; 
    }


    let title_input = document.getElementById('title_search').value;
    if (title_input != '') {
        url += '&title=' + title_input;   
    }


    let min_age_above = document.getElementById('min_age_above').value;
    let min_age_below = document.getElementById('min_age_below').value;
    if (min_age_above != 0 && min_age_above != '') {
        url += '&min_age_above=' + min_age_above;   
    }
    if (min_age_below != 18 && min_age_below != '') {
        url += '&min_age_below=' + min_age_below;   
    }


    let start_date = document.getElementById('start_date').value;
    let end_date = document.getElementById('end_date').value;
    if (start_date != '') {
        url += '&start_date=' + start_date;
    }
    if (end_date != '') {
        url += '&end_date=' + end_date;
    }


    let developerID = document.getElementById('developer_selector').value;
    if (developerID != 'None') {
            url += '&developer_id=' + developerID;  
    }


    let windows = document.getElementById('windows').checked;
    if (windows == false) {
        windows = '';
    }
    else {
        windows = 'w'
    }
    let mac = document.getElementById('mac').checked;
    if (mac == false) {
        mac = '';
    }
    else {
        mac = 'm'
    }
    let linux = document.getElementById('linux').checked;
    if (linux == false) {
        linux = '';
    }
    else {
        linux = 'l'
    }

    let platforms = new Array(windows, mac, linux)
    platforms = platforms.filter(empty_string => {
        return empty_string !== '';
    });
    if (platforms.length != 0) {
        platforms = platforms.toString();
        url += '&platforms=' + platforms;
    }
    

    let price_above = document.getElementById('price_above').value;
    let price_below = document.getElementById('price_below').value;
    if (price_above != '') {
        url += '&price_above=' + price_above;
    }
    if (price_below != '') {
        url += '&price_below=' + price_below; 
    }
    console.log(url)
    let percent_pos_ratings_above = document.getElementById('percent_pos_ratings_above').value;
    let percent_pos_ratings_below = document.getElementById('percent_pos_ratings_below').value;
    if (percent_pos_ratings_above != '') {
        url += '&percent_pos_ratings_above=' + percent_pos_ratings_above;  
    }
    if (percent_pos_ratings_below != '') {
        url += '&percent_pos_ratings_below=' + percent_pos_ratings_below;
    }

    let total_ratings_above = document.getElementById('total_ratings_above').value;
    let total_ratings_below = document.getElementById('total_ratings_below').value;
    if (total_ratings_above != '') {
        url += '&total_ratings_above=' + total_ratings_above;  
    }
    if (total_ratings_below != '') {
        url += '&total_ratings_below=' + total_ratings_below;
    }

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(games) {
        let game_html = '';
        if (games.length == 0) {
            game_html += '<p><strong>No game found 😔 Please try again!</strong></p>'
        }
        for (var i = 0; i < games.length; i++) {
            var game = games[i];
            game_id = game['id']
            game_html += `
            <button class="game_item text_align_left" id="${game_id}" value="${game_id}" onclick="onGameSelected(${game_id})">
                <div class="flex">
                    <img id="header${game_id}" onclick="imgEnlarge(this.id)" class="game_img" alt="Header Image for ${game['title']}" src="${game['media']['header_image']}">
                    <p style="margin-left: 10px;"><strong>${game['title']}</strong><br>${game['description']}</p>
                </div>
            </button>`;
        }

        loading_text_html.style.display = 'none';
    
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
                <img id="header${game_id}" onclick="imgEnlarge(this.id)" class="game_img" alt="Header Image for ${game['title']}" src="${game['media']['header_image']}">
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
            game_html += `<img id="${game_id}+${i}" onclick="imgEnlarge(this.id)" class="game_img" src="${image}">`;
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



function onStatsFilterChanged() {
    var loading_text_html = document.getElementById('loading_stats');
    if (loading_text_html) {
        loading_text_html.innerHTML = 'Loading...';
    } else {
        return
    }

    let url = getAPIBaseURL() + '/stats/?';

    let output = ''
    if (document.getElementById('output_devs').checked) {
        output = 'devs'
    } else if (document.getElementById('output_dates').checked) {
        output = 'dates'
    } else if (document.getElementById('output_ratings').checked) {
        output = 'ratings'
    } else {
        output = 'genres'
    }
    url += 'output=' + output

    let genre_selector = document.getElementById('genre_selector');
    let genreID = genre_selector.value;
    if (genreID != 'None') {
        url += '&genre_id=' + genreID; 
    }


    let title_input = document.getElementById('title_search').value;
    if (title_input != '') {
        url += '&title=' + title_input;   
    }


    let min_age_above = document.getElementById('min_age_above').value;
    let min_age_below = document.getElementById('min_age_below').value;
    if (min_age_above != 0 && min_age_above != '') {
        url += '&min_age_above=' + min_age_above;   
    } if (min_age_below != 18 && min_age_below != '') {
        url += '&min_age_below=' + min_age_below;   
    }


    let start_date = document.getElementById('start_date').value;
    let end_date = document.getElementById('end_date').value;
    if (start_date != '') {
        url += '&start_date=' + start_date;
    } if (end_date != '') {
        url += '&end_date=' + end_date;
    }


    let developerID = document.getElementById('developer_selector').value;
    if (developerID != 'None') {
            url += '&developer_id=' + developerID;  
    }


    let windows = document.getElementById('windows').checked;
    if (windows == false) {
        windows = '';
    } else {
        windows = 'w'
    }
    let mac = document.getElementById('mac').checked;
    if (mac == false) {
        mac = '';
    } else {
        mac = 'm'
    }
    let linux = document.getElementById('linux').checked;
    if (linux == false) {
        linux = '';
    } else {
        linux = 'l'
    }

    let platforms = new Array(windows, mac, linux)
    platforms = platforms.filter(empty_string => {
        return empty_string !== '';
    });
    if (platforms.length != 0) {
        platforms = platforms.toString();
        url += '&platforms=' + platforms;
    }
    

    let price_above = document.getElementById('price_above').value;
    let price_below = document.getElementById('price_below').value;
    if (price_above != '') {
        url += '&price_above=' + price_above;
    } if (price_below != '') {
        url += '&price_below=' + price_below; 
    }

    let percent_pos_ratings_above = document.getElementById('percent_pos_ratings_above').value;
    let percent_pos_ratings_below = document.getElementById('percent_pos_ratings_below').value;
    if (percent_pos_ratings_above != '') {
        url += '&percent_pos_ratings_above=' + percent_pos_ratings_above;  
    } if (percent_pos_ratings_below != '') {
        url += '&percent_pos_ratings_below=' + percent_pos_ratings_below;
    }

    let total_ratings_above = document.getElementById('total_ratings_above').value;
    let total_ratings_below = document.getElementById('total_ratings_below').value;
    if (total_ratings_above != '') {
        url += '&total_ratings_above=' + total_ratings_above;  
    } if (total_ratings_below != '') {
        url += '&total_ratings_below=' + total_ratings_below;
    }

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(stats) {
        if (stats.length == 1) {
            loading_text_html = 'No data found!';
        } else {
            const chart_title = stats['OBJECTIVE_TITLE'];
            delete stats['OBJECTIVE_TITLE']

            loading_text_html.innerHTML = '';

            var chart_title_html = document.getElementById('chart_title');
            if (chart_title_html) {
                chart_title_html.innerHTML = chart_title;
            } else {
                return
            }

            var chart_element = document.getElementById('chart');
            if (chart_element) {
                chart_element = chart_element.getContext('2d');
            } else {
                return
            }

            const data = {
                labels: Object.keys(stats),
                datasets: [{
                    label: chart_title,
                    data: Object.values(stats),
                    backgroundColor: getColors(Object.values(stats).length),
                    hoverOffset: 4
                }]
            };
            

            new Chart(chart_element, {
                type: 'pie',
                data: data,
            });
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

function imgEnlarge(img_id) {
    event.stopPropagation();
    var modal = document.getElementById("imgModal");

    // Get the image and insert it inside the modal - use its "alt" text as a caption
    var img = document.getElementById(img_id);
    var imgEnlarged = document.getElementById("imgEnlarged");
    modal.style.display = "block";
    imgEnlarged.src = img.src;

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() { 
        modal.style.display = "none";
    }
}