function check(zadanie) {
    // TODO funkcja sprawdzająca poprawność zadania
    for (const element of document.getElementsByClassName(zadanie + '-correct')) {
        element.style.color = 'green';
    }
    for (const element of document.getElementsByClassName(zadanie + '-incorrect')) {
        element.style.color = 'red';
    }
}
document.addEventListener('DOMContentLoaded', function() {
    M.Sidenav.init(document.querySelectorAll('.sidenav'));
    M.Materialbox.init(document.querySelectorAll('.materialboxed'));
});

window.MathJax = {
    startup: {
        ready: () => {
            MathJax.startup.defaultReady();
            MathJax.startup.promise.then(() => {
                document.getElementById('mathjax-content').style.opacity = '100';
            });
        }
    }
};
