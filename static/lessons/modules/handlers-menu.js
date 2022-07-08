import { highlightNavMenu } from "./components-nav.js";
import { addWatchlistBtnListener } from "./components-watchlist.js";

function studyMenuHandler() {
    highlightNavMenu();
}

function reviewMenuHandler() {
    highlightNavMenu();
}

function watchlistMenuHandler() { 
    highlightNavMenu();
    addWatchlistBtnListener();
}

export { studyMenuHandler, reviewMenuHandler, watchlistMenuHandler };