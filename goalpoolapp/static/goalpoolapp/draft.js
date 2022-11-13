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
    playercontainer.innerHTML = ""
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
            let player = document.createElement("p")
            player.innerHTML = playerset[i].nickname
            player.classList.add("draftplayer");
            player.addEventListener("click", () => {
                if (confirm(`You are about to pick ${playerset[i].firstname} ${playerset[i].surname}. This cannot be undone`)){
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
            playercontainer.appendChild(player)
        }
    })
})
} catch {
    console.log("If player is not the picker in the draft, or the draft is not in progress some Javascript is not loaded")
}