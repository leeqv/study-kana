import { highlightNavMenu } from "./components-nav.js";
import { addWatchlistBtnListener } from "./components-watchlist.js";
import { show, hide, makeOpaque, makeTransparent } from "./helpers-display.js";

function oldLessonHandler() {
    highlightNavMenu();
    addWatchlistBtnListener();
    addStrokeOrderListener();
}

function newLessonHandler() {
    highlightNavMenu();
    addWatchlistBtnListener();
    addStrokeOrderListener();
    addQuizPromptBtnListener();
}

function endOfLessonHandler() {
    highlightNavMenu();
}

function addStrokeOrderListener() {
    const showStrokeBtn = document.getElementById('showStrokeBtn'),
        hideStrokeBtn = document.getElementById('hideStrokeBtn'),
        strokeDiv = document.getElementById('js-stroke-order-img');
    
    showStrokeBtn.addEventListener('click', function(){
        show(hideStrokeBtn);
        hide(showStrokeBtn);
        makeOpaque(strokeDiv);
    });
    
    hideStrokeBtn.addEventListener('click', function(){
        hide(hideStrokeBtn);
        show(showStrokeBtn);
        makeTransparent(strokeDiv);
    });
}

function addQuizPromptBtnListener() {
    const showPromptBtn = document.getElementById('sure2quiz-prompt'),
        overlay = document.getElementById('go2quiz-overlay'),
        dialogBox = document.getElementById('go2quiz-dialog-box'),
        closePromptBtn = document.getElementById('go2quiz-close');
    showPromptBtn.addEventListener('click', function(){
        show(overlay);
    });
    // Listeners for the prompt elements
    overlay.addEventListener('click', function() {
        hide(overlay);
    });
    dialogBox.addEventListener('click', function(e) {
        e.stopPropagation();
    });
    closePromptBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        hide(overlay);
    });
}

export { oldLessonHandler, newLessonHandler, endOfLessonHandler };