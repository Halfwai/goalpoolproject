window.addEventListener("scroll", () => {
    navbar = document.querySelector("#navbar")
    navmenus = document.querySelectorAll(".nav-menu-container")
    if (this.scrollY == 0){
        navbar.style.backgroundColor = "#371af500"
        navmenus.forEach(navmenu => {
            navmenu.style.backgroundColor = "#371af500"
        })
    } else {
        navbar.style.backgroundColor = "#371af5"
        navmenus.forEach(navmenu => {
            navmenu.style.backgroundColor = "#371af5"
        })
    }
})

const clubs = [
    "Arsenal",
    "Aston Villa",
    "Bournemouth",
    "Brentford",
    "Brighton",
    "Chelsea",
    "Crystal Palace",
    "Everton",
    "Fulham",
    "Leicester",
    "Leeds",
    "Liverpool",
    "Man City",
    "Man Utd",
    "Newcastle",
    "Nott'm Forest",
    "Southampton",
    "Spurs",
    "West Ham",
    "Wolves",
]


try {
    let teamselect = document.querySelector("#teamselect")
    for(let i = 0; i < clubs.length; i++){
        let team = document.createElement("option")
        team.value = clubs[i];
        team.innerHTML = clubs[i];
        teamselect.appendChild(team)
    }
    teamselect.selectedIndex = -1;
    let leagueid = document.querySelector("#leagueid").value;
    teamselect.addEventListener("change", () => {
        let playercontainer = document.querySelector("#players")
        playercontainer.innerHTML = ""
        fetch('playersearch', {
            method: 'PUT',
            headers: {
                'X-CSRFTOKEN': Cookies.get('csrftoken'),
            },
            body: body = JSON.stringify({
                "team": teamselect.value,
                "league": leagueid,
            })
        })
        .then(response => response.json())
        .then(playerset => {
            playerset = playerset.players;
            for(let i = 0; i < playerset.length; i++){
                let player = document.createElement("p")
                player.innerHTML = playerset[i].nickname
                player.classList.add("draftplayer");
                player.addEventListener("click", () => {
                    if (confirm(`You are about to pick ${playerset[i].firstname} ${playerset[i].surname}. This cannot be undone`)){
                        fetch('pickplayer', {
                            method: 'PUT',
                            headers: {
                                'X-CSRFTOKEN': Cookies.get('csrftoken'),
                            },
                            body: body = JSON.stringify({
                                "player": playerset[i],
                                "league": leagueid,
                            })
                        })
                        .then(response => response.json())
                        .then(response => {
                            alert(response.message)
                            location.reload();
                        })
                    }
                })
                playercontainer.appendChild(player)
            }
        })
    })
}
catch {
    console.log("Draft data not loaded")
}

const players = []

    let teamselect = document.querySelector("#globalteamselect")
    for(let i = 0; i < clubs.length; i++){
        let team = document.createElement("option")
        team.value = clubs[i];
        team.innerHTML = clubs[i];
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
                "team": teamselect.value,
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
                player.addEventListener("click", () => {
                    if(players.length >= playerlimit){
                        alert("You have picked the maximum amount of players")
                    } else {
                        addPlayer(player, playerset[i])
                    }
                })                
                for(let j = 0; j < players.length; j++){
                    console.log("yes")
                    if (players[j].playercode == player.playercode){
                        player.style.display = "none";
                    }
                }
                console.log("yes")
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
// }
// catch {
//     console.log("Global data not loaded")
// }

try {
    let startdraftbutton = document.querySelector("#startdraftbutton")
    var confirmIt = function (e) {
        if (!confirm("Are you sure you want to start the draft? New player cannot be added once the draft has started.")) e.preventDefault();
    };
    startdraftbutton.addEventListener('click', confirmIt, false);
} catch {
}

let playerlist = []
let transferplayerset = document.querySelectorAll(".removeplayer")
transferplayerset.forEach(function(player) {
    playerlist.push(player.dataset.value)
    player.addEventListener('click', () => {
        // values.push(player.dataset.value)
        let playerrow = document.getElementById(`${player.dataset.value}`)
        let playername = document.getElementById(`name${player.dataset.value}`).innerHTML
        console.log(playername)
    })
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
    playerteam.innerHTML = teamplayer.realteam;
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



