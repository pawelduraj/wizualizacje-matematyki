function check(zadanie) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", '/quiz', true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    document.getElementById(zadanie).classList.add('disabled')
    for (const element of document.getElementsByClassName(zadanie)) {
        element.previousElementSibling.className = 'check';
        element.previousElementSibling.disabled = true;
    }
    for (const element of document.getElementsByClassName(zadanie + ' correct')) {
        element.style.color = 'green';
        if (element.previousElementSibling.checked) {
            xhr.send("zad=" + zadanie.substring(3, zadanie.length) + "&correct=true");
        } else {
            xhr.send("zad=" + zadanie.substring(3, zadanie.length) + "&correct=false");
        }
    }
    for (const element of document.getElementsByClassName(zadanie + ' incorrect')) {
        element.style.color = 'red';
    }
}

document.addEventListener('DOMContentLoaded', function () {
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
