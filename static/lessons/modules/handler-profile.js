import { highlightNavMenu } from "./components-nav.js";

function profileHandler() {
    highlightNavMenu();
    addProgressBar();
}

/** Profile components */

function addProgressBar() {
    var barH = document.getElementById('bar-hiragana');
    barH.style.width = barH.dataset.percent + "%";

    var barK = document.getElementById('bar-katakana');
    barK.style.width = barK.dataset.percent + "%";
}

export { profileHandler };