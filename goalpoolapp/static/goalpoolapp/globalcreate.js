const countries = [
    "Belgium",
	"France",
	"Croatia",
	"Brazil",
    "Uruguay",
    "Spain",
    "England",
    "Japan",
    "Senegal",
    "Serbia",
    "Switzerland",
    "Mexico",
    "South Korea",
    "Australia",
    "Denmark",
    "Iran",
    "Saudi Arabia",
    "Poland",
    "Germany",
    "Argentina",
    "Portugal",
    "Tunisia",
    "Costa Rica",
    "Morocco",
    "Wales",
    "Netherlands",
    "Ghana",
    "Cameroon",
    "Qatar",
    "Ecuador",
    "USA",
    "Canada",
]

const players = []

let teamselect = document.querySelector("#globalteamselect")
for(let i = 0; i < countries.length; i++){
    let team = document.createElement("option")
    team.value = countries[i];
    team.innerHTML = countries[i];
    teamselect.appendChild(team)
}
teamselect.selectedIndex = -1;
let leagueid = document.querySelector("#leagueid").value;
teamselect.addEventListener("change", () => {
    let playercontainer = document.querySelector("#globalplayers")
    playercontainer.innerHTML = ""
    fetch('playersearch', {
        method: 'PUT',
        headers: {
            'X-CSRFTOKEN': Cookies.get('csrftoken'),
        },
        body: body = JSON.stringify({
            "country": teamselect.value,
            "league": leagueid,
        })
    })
    .then(response => response.json())
    .then(dataset => {
        playerlimit = dataset.playerlimit
        playerset = dataset.players;
        for(let i = 0; i < playerset.length; i++){
            let player = document.createElement("p")
            player.innerHTML = playerset[i].nickname
            player.classList.add("draftplayer");
            player.setAttribute('id',`${playerset[i].playercode}`);
            for(let j = 0; j < players.length; j++){
                if (players[j].playercode == playerset[i].playercode){
                    player.style.display = "none";
                }
            }
            player.addEventListener("click", () => {
                if(players.length >= playerlimit){
                    alert("You have picked the maximum amount of players")
                } else {
                    addPlayer(player, playerset[i])
                }
            })
            playercontainer.appendChild(player)
        }
    })
})
submitglobalteam = document.querySelector("#teamsubmit")
submitglobalteam.addEventListener("click", () => {
    teamname = document.querySelector("#globalteamname")
    if (teamname.value == ""){
        alert("Please input teamname")
    }
    else if (players.length != 10){
        alert("Please pick 10 players")
    }
    else {
        fetch('createglobalteam', {
            method: 'POST',
            headers: {
                'X-CSRFTOKEN': Cookies.get('csrftoken'),
            },
            body: body = JSON.stringify({
                "teamname": teamname.value,
                "players": players,
            })
        })
        .then(response => response.json())
        .then(dataset => {
            alert(dataset.message)
            if (dataset.route === 'globalleague'){
                window.location.href = `${dataset.route}`
            }
        })
    }
})

function addPlayer(player, teamplayer){
    players.push(teamplayer)
    player.style.display = "none"
    let cancel = document.createElement("i")
    cancel.classList.add("fa-solid", "fa-circle-minus", "fa-xl")
    let row = document.createElement("tr")
    let playername = document.createElement("td")
    playername.innerHTML = teamplayer.nickname;
    let playerteam = document.createElement("td")
    playerteam.innerHTML = countries[teamplayer.country_id - 1];
    let goals = document.createElement("td")
    goals.innerHTML = teamplayer.goals;
    table = document.querySelector("#pickplayertable")
    row.appendChild(cancel)
    row.appendChild(playername)
    row.appendChild(playerteam)
    row.appendChild(goals)
    table.appendChild(row)
    cancel.addEventListener("click", () => {
        removePlayer(players, playername, player, row)
    })
}

function removePlayer(players, playername, player, row) {
    for (let j = players.length -1; j >=0 ; j--){
        if (players[j].nickname == playername.innerHTML){
            players.splice(j, 1);
        }
    }
    row.remove();
    player.style.display = "block";
}