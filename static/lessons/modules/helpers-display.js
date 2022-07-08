function hide(...elements) { 
    elements.forEach(el => {
        el.classList.add('u-hidden');
        el.setAttribute('aria-hidden', 'true');
    });
}

function show(...elements) { 
    elements.forEach(el => {
        el.classList.remove('u-hidden');
        el.setAttribute('aria-hidden', 'false');
    });
}

function makeTransparent(...elements) { 
    elements.forEach(el => {
        el.classList.add('u-transparent');
        el.setAttribute('aria-hidden', 'true');
    });
}

function makeOpaque(...elements) { 
    elements.forEach(el => {
        el.classList.remove('u-transparent');
        el.setAttribute('aria-hidden', 'false');
    });
}

export { hide, show, makeTransparent, makeOpaque };