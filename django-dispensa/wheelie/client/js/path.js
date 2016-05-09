(function() {
    var path = document.querySelector('#menu-path-line');
    var menu = document.querySelector('.menu');

    if (!path || !menu) {
        return;
    }

    var pathLength = path.getTotalLength();
    var menuHeight = menu.offsetHeight;
    var referenceTop = menu.offsetTop;

    path.style.strokeDashoffset = pathLength;

    window.addEventListener("scroll", function() {

        var scrollPercentage = (window.pageYOffset - referenceTop) / ((menuHeight - window.innerHeight) + 450);
        var drawLength = (pathLength * scrollPercentage);

        path.style.strokeDashoffset = pathLength - drawLength;

        if (scrollPercentage >= 0.99) {
            path.style.strokeDasharray = "none";
        } else {
            path.style.strokeDasharray = pathLength + ' ' + pathLength;
        }
    });
})();
