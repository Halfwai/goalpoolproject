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

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// Draft page loading
try {
    let teamselect = document.querySelector("#teamselect")
    for(let i = 0; i < countries.length; i++){
        let team = document.createElement("option")
        team.value = countries[i];
        team.innerHTML = countries[i];
        teamselect.appendChild(team)
    }
    teamselect.selectedIndex = -1;
    let leagueid = document.querySelector("#leagueid").value;
teamselect.addEventListener("change", () => {
    let playercontainer = document.querySelector("#players")
    playercontainer.style.display = "flex"
    playercontainer.innerHTML = ""
    const positions = ['goalkeepers', 'defenders', 'midfielders', 'attackers']
    for (let i = 0; i < positions.length; i++) {
        let title = document.createElement("h4")
        let playerbox = document.createElement("div")
        title.innerHTML = capitalizeFirstLetter(positions[i])
        playerbox.classList.add("playersbox");
        playerbox.setAttribute('id', positions[i]);
        playercontainer.appendChild(title)
        playercontainer.appendChild(playerbox)
    }
    fetch('../playersearch', {
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
    .then(playerset => {
        playerset = playerset.players;
        for(let i = 0; i < playerset.length; i++){
            let player = document.createElement("div")
            let playerpic = document.createElement("img")
            let playername = document.createElement("div")
            playerpic.src = playerset[i].pic
            playerpic.classList.add("playerpic");
            playername.innerHTML = playerset[i].nickname
            player.appendChild(playerpic)
            player.appendChild(playername)
            player.classList.add("draftplayer");
            player.addEventListener("click", () => {
                if (confirm(`You are about to pick ${playerset[i].nickname}. This cannot be undone`)){
                    fetch('../pickplayer', {
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
            if (playerset[i].position === "Goalkeeper"){
                goalkeepers.appendChild(player)
            } else if (playerset[i].position === "Defender") {
                defenders.appendChild(player)
            } else if (playerset[i].position === "Midfielder") {
                midfielders.appendChild(player)
            } else if (playerset[i].position === "Attacker") {
                attackers.appendChild(player)
            }
        }
    })
})
} catch {
    // If player is not the picker in the draft, or the draft is not in progress some Javascript is not loaded
}