let api_headers = {
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    headers: {
        "Content-Type": "application/json",
    },
    redirect: "follow",
    referrerPolicy: "no-referrer"
};

let coins = [];

function update_prices(){
    for(c in coins){
        let coin = coins[c];
        for(e in coin.exchanges){
            let exchange = coin.exchanges[e];
            fetch_api(exchange);
        }
    }
}

function fetch_api(exchange) {
    fetch(exchange.url, api_headers)
    .then((response) => response.json())
    .then((result) => {
        let prices = [];
        let dates = [];
        for (r in result) {
            let data = result[r];
            prices[prices.length] = data.price;
            dates[dates.length] = data.datetime;
        }
        exchange.prices = prices;
        exchange.dates = dates;
    });
}

function draw_charts() {
    Array.from(coins).forEach(graph => draw(graph));
}

function draw(graph){
    console.log(graph);
    const ctx = document.getElementById(graph.name);
    let l = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'];
    let o = {
        type: 'line',
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1
    };
    let d =[];
    Array.from(graph.exchanges).forEach(exchange => {
        l = exchange.dates;
        p = Object.create(o);
        p.type = "line";
        p.label = exchange.name;
        p.data = exchange.prices;
        p.borderWidth = 1;
        d.push(p);
    });
    new Chart(ctx, {
        data: {
        type: 'line',
            labels: l,
            datasets: d,
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

async function run(){
    await fetch('./static/config.json')
    .then((config_file) => {
        return config_file.json();
    })
    .then((json_config) => {
        json_config.coins.forEach(c => {
            let exchanges = [];
            json_config.exchanges.forEach(e => {
                let exchange = { "name": e.name, "url": e.url  + "?symbol=" + encodeURIComponent(c) + "&filter=" + encodeURIComponent(json_config.filters), "prices": [], "dates": []};
                exchanges.push(exchange);
            });
            let coin = { "name": c, "exchanges": exchanges };
            coins[coins.length] = coin;
        });
    });
}

function reload(){
    location.reload();
}

run();

setTimeout(update_prices, 10);
setTimeout(draw_charts, 100);
setTimeout(reload, 60000 * 60);