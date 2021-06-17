function check(zadanie) {
    // TODO funkcja sprawdzająca poprawność zadania
    for (const element of document.getElementsByClassName(zadanie + '-correct')) {
        element.style.color = 'green';
    }
    for (const element of document.getElementsByClassName(zadanie + '-incorrect')) {
        element.style.color = 'red';
    }
}
