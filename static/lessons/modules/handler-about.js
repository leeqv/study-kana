function aboutPageHandler() {
    const header = document.getElementById('js-header');
    window.addEventListener('scroll', function toggleFixedHeader() {
        if (window.scrollY > window.innerHeight * 0.5) {
            header.classList.add('u-fixed-header');
        } else {
            header.classList.remove('u-fixed-header');
        }
    });

    // video hover play
    const snippets = document.querySelectorAll('.js-snippet-video:not(.u-hidden)');
    [...snippets].forEach(snippet => {
        snippet.addEventListener('mouseover', function() {
            this.play();
            this.parentElement.querySelector('.js-snippet-play-icon').classList.add('u-hidden');
        });
        snippet.addEventListener('mouseout', function() {
            this.load();
            this.parentElement.querySelector('.js-snippet-play-icon').classList.remove('u-hidden');
        });
    });
}

export { aboutPageHandler };