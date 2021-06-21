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
    M.Dropdown.init(document.querySelectorAll('.dropdown-trigger'),
        {
            alignment: 'center',
            autoTrigger: false,
            coverTrigger: false,
            hover: true
        });
    M.Collapsible.init(document.querySelectorAll('.collapsible'));
    M.Sidenav.init(document.querySelectorAll('.sidenav'));
    M.Materialbox.init(document.querySelectorAll('.materialboxed'));
});
