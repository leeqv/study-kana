import { getSectionName, getCookie } from "./helpers-others.js";
import { show, hide, makeTransparent, makeOpaque } from "./helpers-display.js";

function addWatchlistBtnListener() {
    let watchlistBtns = document.getElementsByClassName('js-watchlist-btn');
    for (let btn of watchlistBtns) {
        btn.addEventListener('click', function() {
            updateWatchlist(btn.dataset.letter, btn);
        });
    }
}

function updateWatchlist(letterKana, watchlistBtn) { 
    sessionStorage.setItem('undo-watchlist-letter', letterKana);
    
    fetch(`/update_watchlist/`, {
        method: "POST",
        mode: 'same-origin',  
        //credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            letter: letterKana,
        })
    })
    .then(response => response.json())
    .then(result => {  
        var sectionName = getSectionName();
        // PATH is watchlist      
        if (sectionName === 'watchlist') {
            const currentLetterDiv = document.getElementById(`letterDiv-${letterKana}`),
                alertDiv = document.getElementById('alert-watchlist'),
                alertText = document.getElementById('alert-text'),
                undoBtn = document.getElementById('undo-watchlist-btn');
            alertDiv.classList.add('alert--visible');
            if (result.update === 'added') {
                makeOpaque(currentLetterDiv);
                hide(undoBtn);
                alertText.innerText = `『${letterKana}』 successfully added back to watchlist.`;
            } else if (result.update === 'removed') {
                makeTransparent(currentLetterDiv);
                show(alertDiv, undoBtn);
                alertText.innerText = `『${letterKana}』 successfully removed from watchlist.`;

                // Undo update watchlist
                undoBtn.addEventListener('click', function () {
                    updateWatchlist(sessionStorage.getItem('undo-watchlist-letter'));
                });
            }

            alertDiv.addEventListener('animationend', function() {
                alertDiv.classList.remove('alert--visible');
                hide(alertDiv);
            });
        }
        // PATH is study or review
        else {
            const watchlistBtnText = document.getElementById('js-watchlist-btn-text');
            if (result.update === 'added') {
                watchlistBtn.setAttribute("title", "Remove from watchlist");
                watchlistBtnText.innerText = 'Remove';
            } else if (result.update === 'removed') {
                watchlistBtn.setAttribute("title", "Add to watchlist");
                watchlistBtnText.innerText = 'Add';
            }
        }  
    });
}

export { addWatchlistBtnListener };