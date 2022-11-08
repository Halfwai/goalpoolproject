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

try {
    let startdraftbutton = document.querySelector("#startdraftbutton")
    var confirmIt = function (e) {
        if (!confirm("Are you sure you want to start the draft? New player cannot be added once the draft has started.")) e.preventDefault();
    };
    startdraftbutton.addEventListener('click', confirmIt, false);
} catch {
}

// hamburgermenu for tablets and phones
const menuButton = document.querySelector("#hamburgericon");
const closeButton = document.querySelector("#closeicon");
const dropdown = document.querySelector("#hamburgermenu");
// opens menu when hamburger icon clicked and replaces hamburger icon with close menu icon 
menuButton.addEventListener('click', () => {
    dropdown.style.display = "flex";
    menuButton.style.display = "none";
    closeButton.style.display = "block";
});
// closes menu when close menu icon clicked and replaces with hamburger icon
closeButton.addEventListener('click', () => {
    dropdown.style.display = "none";
    menuButton.style.display = "block";
    closeButton.style.display = "none";
});

// closes all hamburger menus when window is expanded above 780px, and displays hamburger menu icon when window is shrunk below this.
window.addEventListener("resize", () => {
    if(window.innerWidth > 780){
        dropdown.style.display = "none";
        menuButton.style.display = "none";
        closeButton.style.display = "none";
    } else {
        menuButton.style.display = "block";
    }
});

try {
    let draftmenuopen = document.querySelector("#draftmenudown")
    let draftmenuclose = document.querySelector("#draftmenuup")
    draftmenuopen.addEventListener("click", () => {
        let draftmenus = document.querySelector("#draftleagueitems")
        draftmenus.style.display = "block";
        draftmenuopen.style.display = "none";
        draftmenuclose.style.display = "block";
    })
    draftmenuclose.addEventListener("click", () => {
        let draftmenus = document.querySelector("#draftleagueitems")
        draftmenus.style.display = "none";
        draftmenuopen.style.display = "block";
        draftmenuclose.style.display = "none";
    })
} catch {
    console.log("User not logged in")
}

const logo = document.querySelector("#site-logo");
logo.addEventListener("click", () => {
    location.href = "/";
});



