import { getSectionName } from "./helpers-others.js";

function highlightNavMenu() {
    var navMenu = document.getElementById(`menu-${getSectionName()}`);
    navMenu.classList.add('u-highlighted-menu');
}

function sideNavHandler() {
    const hambBtn = document.querySelector('#js-hamburger-btn');
    hambBtn.addEventListener('click', function changeHambAnimation() {
        hambBtn.classList.toggle('hamb-entrance');
    });

    const toggleBtn = document.getElementById('toggle-nav');
    var mediaQuery800px = window.matchMedia('(min-width: 800px)');
    mediaQuery800px.addEventListener('change', hideToggleBtnAtWideScreen);
    function hideToggleBtnAtWideScreen(minWidth) {
        if (minWidth.matches) { // If media query matches
            toggleBtn.checked = false;
            hambBtn.classList.remove('hamb-entrance');
        }
    }
}

export { highlightNavMenu, sideNavHandler };