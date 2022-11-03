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
try {
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
                if(!players.includes(playerset[i])){
                    let player = document.createElement("p")
                    player.innerHTML = playerset[i].nickname
                    player.classList.add("draftplayer");
                    player.setAttribute('id',`${playerset[i].playercode}`);
                    player.addEventListener("click", () => {
                        if(players.length >= playerlimit){
                            alert("You have picked the maximum amount of players")
                        } else {
                            players.push(playerset[i])
                            playerbutton = document.getElementById(playerset[i].playercode)
                            playerbutton.remove()
                            let cancel = document.createElement("i")
                            cancel.classList.add("fa-solid", "fa-circle-minus", "fa-xl")
                            cancel.addEventListener("click", () => {
                                console.log("yes")
                                for(let j = players.length-1; j >= 0; j--){
                                    if (playerset[i] === players[j]){
                                        players.splice(j, 1)
                                        playerrow = document.getElementById(`table${playerset[i].playercode}`)
                                        playerrow.remove()
                                    }
                                }
                            })
                            let row = document.createElement("tr")
                            row.setAttribute('id',`table${playerset[i].playercode}`);
                            let teamplayer = document.createElement("td")
                            teamplayer.innerHTML = playerset[i].nickname;
                            let playerteam = document.createElement("td")
                            playerteam.innerHTML = playerset[i].realteam;
                            let goals = document.createElement("td")
                            goals.innerHTML = playerset[i].goals;
                            table = document.querySelector("#pickplayertable")
                            row.appendChild(cancel)
                            row.appendChild(teamplayer)
                            row.appendChild(playerteam)
                            row.appendChild(goals)
                            table.appendChild(row)
                        }
                    })
                    playercontainer.appendChild(player)
                }
            }
        })
    })
}
catch {
    console.log("Draft data not loaded")
}

