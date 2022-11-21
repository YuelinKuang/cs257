// webapp.js
// Yuelin Kuang and Lucie Wolf 
// Nov 9, 2022
// Revised on Nov 21, 2022
// Web Appilication project for CS 257. 

window.onload = initialize;

function initialize() {
    loadGenresSelector();
    loadDevelopersSelector();
    loadMainPageImages();

    let games_search_button = document.getElementById('games_search_button');
    if (games_search_button) {
        games_search_button.onclick = onGamesFilterChanged;
    }

    let stats_search_button = document.getElementById('stats_search_button');
    if (stats_search_button) {
        stats_search_button.onclick = onStatsFilterChanged;
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

// Loads the list of genre options into the genre selector.
function loadGenresSelector() {
    // Tests whether the genre_selector is on the current page. 
    // If it's not, skip this function. 
    let genre_elector = document.getElementById('genre_selector');
    if (genre_elector) {
        genre_elector.innerHTML = '';
    } else {
        return;
    }

    let url = getAPIBaseURL() + '/genres';

    // Send the request to the API /genres endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of genre dictionaries).
    .then((response) => response.json())

    .then(function(genres) {
        // Add the <option> elements to the <select> element
        let selectorBody = '<option value="None">Any</option>\n';
        for (let k = 0; k < genres.length; k++) {
            let genre = genres[k];
            selectorBody += '<option value="' + genre['id'] + '">' + genre['genre_name'] + '</option>\n';
        }

        genre_elector.innerHTML = selectorBody;
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

// Loads the list of developer options into the developer selector.
function loadDevelopersSelector() {
    // Tests whether the developer_selector is on the current page. 
    // If it's not, skip this function. 
    let developer_selector = document.getElementById('developer_selector');
    if (developer_selector) {
        developer_selector.innerHTML = '';
    } else {
        return; 
    }

    let url = getAPIBaseURL() + '/developers';

    // Send the request to the API /developers endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of developer dictionaries).
    .then((response) => response.json())

    .then(function(developers) {
        // Add the <option> elements to the <select> element
        let selectorBody = '<option value="None">Any</option>\n';
        for (let k = 0; k < developers.length; k++) {
            let developer = developers[k];
            selectorBody += '<option value="' + developer['id'] + '">' 
                            + developer['developer_name'] + '</option>\n';
        }

        developer_selector.innerHTML = selectorBody;
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

// Loads some images to be displayed on the main page. 
function loadMainPageImages() {
    let url = getAPIBaseURL() + '/main_page_images';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(games) {
        let main_page_images_body = '';
        for (let k = 0; k < games.length; k++) {
            let game = games[k];
            let game_id = game['id']
            let header_image = game['media']['header_image']
            main_page_images_body += `<img id="header${game_id}" class="game_img" src="${header_image}">`;
        }

        let main_page_image_container = document.getElementById('main_page_image_container');
        if (main_page_image_container) {
            main_page_image_container.innerHTML = main_page_images_body;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

// Reads in the filters entered by the user on the games_main page, 
// gets the list of relevant games, and displays the header image, 
// title, and short description of each game in an organized format.
function onGamesFilterChanged() {
    // Tests whether the games_container is on the current page.
    // If it's not, skip this function. 
    var games_container = document.getElementById('games_container');
    if (games_container) {
        games_container.innerHTML = '';
    } else {
        return; 
    }

    // Displays a message showing that the page is loading. 
    var loading_text_html = document.getElementById('loading_games');
    if (loading_text_html) {
        loading_text_html.innerHTML = 'Loading...';
    }

    // Builds the sort_by parameter. 
    // sort_by=title-asc is the default. 
    let sort_by = ''
    if (document.getElementById('sort_date').checked) {
        sort_by = 'date'
    } else if (document.getElementById('sort_price').checked) {
        sort_by = 'price'
    } else if (document.getElementById('sort_age').checked) {
        sort_by = 'age'
    } else if (document.getElementById('sort_pos_ratings').checked) {
        sort_by = 'pos_ratings'
    } else {
        sort_by = 'title'
    }
    if (document.getElementById('sort_desc').checked){
        sort_by += '-desc'
    } else {
        sort_by += '-asc'
    }

    // Appends the formatted string containing all relevant GET parameters to the URL
    let url = `${getAPIBaseURL()}/games?sort_by=${sort_by}${addFiltersToURL()}`;

    // Send the request to the API /games endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of game dictionaries).
    .then((response) => response.json())

    .then(function(games) {
        let game_html = '';

        // If there is no game found: 
        if (games.length == 0) {
            game_html += '<p>No games found 😔 Please try again!</p>'
        }

        // If there are games found, build the html for the games_container with the games information
        for (var i = 0; i < games.length; i++) {
            var game = games[i];
            game_id = game['id']

            // The onclick event is added to make each game item expandable on click. 
            game_html += 
                `<button class="game_item text_align_left" id="${game_id}" value="${game_id}" onclick="onGameSelected(${game_id})">
                    <div>
                        <img id="header${game_id}" class="game_img" src="${game['header_image']}">`
            
            // If there is website information, link the title of the game to the website. 
            if (game['website'] == 'N/A' || game['website'] == '') {
                game_html += 
                    `<p>
                        ${game['title']}
                    </p></div>
                    <p>${game['description']}</p>`
            } else {
                game_html += 
                    `<p>
                        <a href="${game['website']}" target="_blank" onclick="event.stopPropagation();">
                            ${game['title']}
                        </a>
                    </p></div>
                    <p>${game['description']}</p>`
            }
                
            game_html += `</button>`;
        }
        // Removes the loading message. 
        loading_text_html.innerHTML = '';

        games_container.innerHTML = game_html;

        // Displays an enlarged view in modal for every image on click. 
        addOnclickListenerForAllImages();
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

// Displays the detail information of a specific game selected whose id equals game_id.
function onGameSelected(game_id) {
    let url = getAPIBaseURL() + '/games/specific/' + game_id; 
    
    // Send the request to the API /games/specific/<game_id> endpoint
    fetch(url, {method: 'get'})

    // When the result comes back, transform it from a JSON string into
    // a Javascript object (in this case, a dictionary with detail information of the game).
    .then((response) => response.json())

    .then(function(game) {
        // Turns all the 'true' values to '√' and 'false' values to 'X'
        for (trait in game){
            let value = String(game[trait]);
            if (value == 'true') {
                game[trait] = '√'
            } else if (value == 'false') {
                game[trait] = 'X'
            }
        }

        // If there is no information about minimum age, the value is stored as '0' 
        // This is a limitation of the original dataset. 
        if (game['minimum_age'] == 0) {
            game['minimum_age'] = '0 or unlisted';
        }

        // Starts building the html body for the specific game item selected
        // The onclick event is added to make the selected game item collapsible on click.
        let game_html = '';
        game_html += 
                `<button class="game_item text_align_left" id="${game_id}" value="${game_id}" onclick="onGameDeselected(${game_id})">
                    <div>
                        <img id="header${game_id}" class="game_img" src="${game['media']['header_image']}">`
            
            // If there is website information, link the title of the game to the website. 
            if (game['website'] == 'N/A' || game['website'] == '') {
                game_html += 
                    `<p>
                        ${game['title']}
                    </p></div>
                    <p>${game['description']}</p>`
            } else {
                game_html += 
                    `<p>
                        <a href="${game['website']}" target="_blank" onclick="event.stopPropagation();">
                            ${game['title']}
                        </a>
                    </p></div>
                    <p>${game['description']}</p>`
            }

        game_html +=
        `</div>
            <div>
                <div> 
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
                <div class="image_group">`;

        // Selects the first six screenshots to display
        let images = game['media']['screenshots'];
        for (var i = 0; i < images.length && i < 6; i++) {
            var image = images[i];
            game_html += `<img id="${game_id}+${i}" class="game_img" src="${image}">`;
        }
        
        game_html += '</div></div></button>'

        // Replaces the original html body with the new one, which is an expanded version
        // containing detail information about the specific game. 
        // The outerHTML is replaced because the onclick function changes. 
        var selected_game_item = document.getElementById(game_id);
        if (selected_game_item) {
            selected_game_item.outerHTML = game_html;
        }

        // Displays an enlarged view in modal for every image on click. 
        addOnclickListenerForAllImages();
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

// Displays only the header image, title, and short description of 
// a specific game deselected whose id equals game_id.
function onGameDeselected(game_id) {
    let url = getAPIBaseURL() + '/games/specific/' + game_id; 
    
    // Send the request to the API /games/specific/<game_id> endpoint
    fetch(url, {method: 'get'})

    // When the result comes back, transform it from a JSON string into
    // a Javascript object (in this case, a dictionary with detail information of the game).
    // Note that only the relevant information (header image, title, and description) will be used. 
    .then((response) => response.json())

    .then(function(game) {
        // Same as in onGamesFilterChanged(), the onclick event is added to make each game item 
        // expandable on click. 
        let game_html = `
            <button class="game_item text_align_left" id="${game_id}" value="${game_id}" onclick="onGameSelected(${game_id})">
                <div>
                    <img id="header${game_id}" class="game_img" src="${game['media']['header_image']}">`
        
        // If there is website information, link the title of the game to the website. 
        if (game['website'] == 'N/A' || game['website'] == '') {
            game_html += 
                `<p>
                    ${game['title']}
                </p></div>
                <p>${game['description']}</p>`
        } else {
            game_html += 
                `<p>
                    <a href="${game['website']}" target="_blank" onclick="event.stopPropagation();">
                        ${game['title']}
                    </a>
                </p></div>
                <p>${game['description']}</p>`
        }
            
        game_html += `</button>`;
        
        // Replaces the original html body with the new one, which is an collapsed version
        // containing only the header image, title, and short description of the specific game. 
        // The outerHTML is replaced because the onclick function changes. 
        var deselected_game_button = document.getElementById(game_id);
        if (deselected_game_button) {
            deselected_game_button.outerHTML = game_html;
        }

        // Displays an enlarged view in modal for every image on click. 
        addOnclickListenerForAllImages();
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}


// Reads in the filters entered by the user on the stats_main page, 
// gets the statistics to construct the graphs, and displays the graph
function onStatsFilterChanged() {
    var chart_container_html = document.getElementById('chart_container');
    var chart_element = document.getElementById('chart');

    // Tests whether chart_container_html and chart_element are on the current page. 
    // If they are not, skip this function. 
    if (chart_element) {
        chart_element.remove();
        if (chart_container_html) {
            chart_container_html.innerHTML += '<canvas id="chart"></canvas>'
        } else {
            return
        }
    } else {
        return
    }

    var loading_text_html = document.getElementById('loading_stats');
    var chart_title_html = document.getElementById('chart_title');
    var chart_element = document.getElementById('chart');

    // Displays the loading message. 
    if (loading_text_html) {
        loading_text_html.innerHTML = 'Loading...';
    } else {
        return
    }
    
    // Tests whether chart_title_html is on the current page. 
    // If it's not, skip this function. 
    if (chart_title_html) {
        chart_title_html.innerHTML = '';
    } else {
        return
    }
    

    // Checks which output format is selected: 
    if (document.getElementById('output_devs').checked) {
        output = 'devs';
        chart_type = 'pie';
    } else if (document.getElementById('output_ratings').checked) {
        output = 'ratings';
        chart_type = 'bar';
    } else {
        output = 'genres'
        chart_type = 'pie'
    }
    
    // Appends the formatted string containing all relevant GET parameters to the URL
    let url = `${getAPIBaseURL()}/stats?output=${output}${addFiltersToURL()}`;

    // Send the request to the API /stats endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a dictionary with the graph title and all relevant data).
    .then((response) => response.json())

    .then(function(stats) {
        if (Object.keys(stats).length <= 1) {
            loading_text_html.innerHTML = 'No data found!';
        } else {
            const chart_title = stats['OBJECTIVE_TITLE'];
            delete stats['OBJECTIVE_TITLE']

            if (chart_type == 'pie') {
                const data = {
                    labels: Object.keys(stats),
                    datasets: [{
                        data: Object.values(stats),
                        backgroundColor: getColors(Object.values(stats).length),
                        hoverOffset: 4
                    }]
                };
    
                new Chart(chart_element, {
                    type: 'pie',
                    data: data,
                    options: {
                        plugins: {
                            tooltip: true,
                        },
                        legend: {
                            display: false,
                        }
                      }
                });
            } else {
                //https://www.w3docs.com/snippets/javascript/how-to-find-the-min-max-elements-in-an-array-in-javascript.html
                const min = 0;
                const max = 100;
                const num_bins = 20;
                const bin_size = (max - min) / num_bins;
                let bin_labels = [];
                

                let bins = {}
                for (let i = min; i < max; i += bin_size) {
                    bins[i] = 0;
                    bin_labels.push(`${i}%-${i + bin_size}%`);
                }
                
                for (stat in stats) {
                    for (bin in bins) {
                        if (stat > bin && stat < bin + bin_size) {
                            bins[bin] += stats[stat];
                        }
                    }
                }

                const chart = document.getElementById('chart').getContext('2d');

                new Chart(chart, {
                type: 'bar',
                data: {
                    labels: bin_labels,
                    datasets: [{
                        label: 'Number of Ratings',
                        data: Object.values(bins),
                        backgroundColor: 'rgb(247, 172, 172)',
                        barPercentage: 1.3
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    },
                    legend: {
                        display: false,
                    }
                }
                });
                
            }
            chart_title_html.innerHTML = chart_title;
            loading_text_html.innerHTML = '';
        }   
    })
    .catch(function(error) {
        console.log(error);
    });
}

// Function adapted from https://stackoverflow.com/questions/12802739/deselect-selected-options-in-select-menu-with-multiple-and-optgroups
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

// Function adapted from https://www.w3schools.com/howto/howto_css_modal_images.asp
function imgEnlarge(img_id) {
    event.stopPropagation();
    var modal = document.getElementById("imgModal");

    // Get the image and insert it inside the modal
    var img = document.getElementById(img_id);
    var imgEnlarged = document.getElementById("imgEnlarged");
    modal.style.display = "block";
    imgEnlarged.src = img.src;

    // Get the <span> element that closes the modal
    var span = document.getElementById("close");

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() { 
        modal.style.display = "none";
    }
}

// Iterates through all images on the page and adds a click event 
// listener for each image so that they can be displayed in modal. 
function addOnclickListenerForAllImages() {
    var imageNodes = document.getElementsByTagName('img');
    for (var i=0; i<imageNodes.length; i++){          
        imageNodes[i].addEventListener('click', function() {
            imgEnlarge(this.id);
        });
    }
}

// Function adapted from https://stackoverflow.com/questions/28828915/how-set-color-family-to-pie-chart-in-chart-js
function getColors(length) {
    let pallet = ["#0074D9", "#FF4136", "#2ECC40", "#FF851B", "#7FDBFF", "#B10DC9", "#FFDC00", "#001f3f", "#39CCCC", "#01FF70", "#85144b", "#F012BE", "#3D9970", "#111111", "#AAAAAA"];
    let colors = [];

    for (let i = 0; i < length; i++) {
        colors.push(pallet[i % (pallet.length - 1)]);
    }

    return colors;
}

// Reads in the filters entered by the user and returns a formatted string 
// that contains only the relevant GET parameters (excluding sort_by). 
function addFiltersToURL() {
    getParameters = ''

    let genre_selector = document.getElementById('genre_selector');
    let genreID = genre_selector.value;
    if (genreID != 'None') {
        getParameters += '&genre_id=' + genreID; 
    }

    let title_input = document.getElementById('title_search').value;
    if (title_input != '') {
        getParameters += '&title=' + title_input;   
    }

    let min_age_above = document.getElementById('min_age_above').value;
    let min_age_below = document.getElementById('min_age_below').value;
    if (min_age_above != 0 && min_age_above != '') {
        url += '&min_age_above=' + min_age_above;   
    } if (min_age_below != 18 && min_age_below != '') {
        getParameters += '&min_age_below=' + min_age_below;   
    }

    let start_date = document.getElementById('start_date').value;
    let end_date = document.getElementById('end_date').value;
    if (start_date != '') {
        getParameters += '&start_date=' + start_date;
    } if (end_date != '') {
        getParameters += '&end_date=' + end_date;
    }

    let developerID = document.getElementById('developer_selector').value;
    if (developerID != 'None') {
        getParameters += '&developer_id=' + developerID; 
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
        getParameters += '&platforms=' + platforms;
    }

    let price_above = document.getElementById('price_above').value;
    let price_below = document.getElementById('price_below').value;
    if (price_above != '') {
        getParameters += '&price_above=' + price_above;
    } if (price_below != '') {
        getParameters += '&price_below=' + price_below; 
    }

    let percent_pos_ratings_above = document.getElementById('percent_pos_ratings_above').value;
    let percent_pos_ratings_below = document.getElementById('percent_pos_ratings_below').value;
    if (percent_pos_ratings_above != '') {
        getParameters += '&percent_pos_ratings_above=' + percent_pos_ratings_above;  
    } if (percent_pos_ratings_below != '') {
        getParameters += '&percent_pos_ratings_below=' + percent_pos_ratings_below;
    }

    let total_ratings_above = document.getElementById('total_ratings_above').value;
    let total_ratings_below = document.getElementById('total_ratings_below').value;
    if (total_ratings_above != '') {
        getParameters += '&total_ratings_above=' + total_ratings_above;  
    } if (total_ratings_below != '') {
        getParameters += '&total_ratings_below=' + total_ratings_below;
    }

    return getParameters
}