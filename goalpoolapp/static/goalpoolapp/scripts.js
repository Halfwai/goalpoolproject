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

// const clubs = [
//     "Arsenal",
//     "Aston Villa",
//     "Bournemouth",
//     "Brentford",
//     "Brighton",
//     "Chelsea",
//     "Crystal Palace",
//     "Everton",
//     "Fulham",
//     "Leicester",
//     "Leeds",
//     "Liverpool",
//     "Man City",
//     "Man Utd",
//     "Newcastle",
//     "Nott'm Forest",
//     "Southampton",
//     "Spurs",
//     "West Ham",
//     "Wolves",
// ]

try {
    let startdraftbutton = document.querySelector("#startdraftbutton")
    var confirmIt = function (e) {
        if (!confirm("Are you sure you want to start the draft? New player cannot be added once the draft has started.")) e.preventDefault();
    };
    startdraftbutton.addEventListener('click', confirmIt, false);
} catch {
}



