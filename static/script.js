function check(zadanie) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", '/quiz', true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            console.log('request has been sent')
        }
    }

    for (const element of document.getElementsByClassName(zadanie)) {
        element.previousElementSibling.className = 'check';
        element.previousElementSibling.disabled = true;
    }
    for (const element of document.getElementsByClassName(zadanie + ' correct')) {
        element.style.color = 'green';
        if (element.previousElementSibling.checked) {
            console.log(zadanie + ' is correct :)');
            xhr.send("zad="+zadanie.substring(3, zadanie.length)+"&correct=true");
        } else {
            console.log(zadanie + ' is incorrect...');
            xhr.send("zad="+zadanie.substring(3, zadanie.length)+"&correct=false");
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
