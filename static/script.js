function check(zadanie) {
    for (const element of document.getElementsByClassName(zadanie)) {
        element.previousElementSibling.className = 'check';
        element.previousElementSibling.disabled = true;
    }
    for (const element of document.getElementsByClassName(zadanie + ' correct')) {
        element.style.color = 'green';
        if (element.previousElementSibling.checked) {
            console.log(zadanie + ' is correct :)')
        } else {
            console.log(zadanie + ' is incorrect...')
        }
    }
    for (const element of document.getElementsByClassName(zadanie + ' incorrect')) {
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
