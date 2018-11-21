function reveal(index) {
    var chapters = Array.from(document.getElementsByClassName('chapter'));
    chapters.forEach(function(element) {
        element.style.visibility = 'hidden';
    });
    document.getElementById(index).style.visibility = 'visible';   
}
var actions = Array.from(document.getElementsByClassName('action'));
actions.forEach(function(element) {
    var target = parseInt(element.getAttribute('href').replace('#', ''));
    element.onclick = function() {reveal(target);};
});