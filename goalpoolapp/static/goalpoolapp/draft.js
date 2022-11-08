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

// Draft page loading
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

