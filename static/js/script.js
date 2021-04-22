let nav = document.querySelector("nav");
let offset = nav.getBoundingClientRect();

if ((offset.top - 80) < 0) {
    nav.classList.remove('nav__scroll')
} else {
    nav.classList.add('nav__scroll')
}


document.addEventListener("DOMContentLoaded", function () {
    document.onscroll = function (e) {
        let scrollStart = e.target.scrollingElement.scrollTop;
        if (scrollStart > (offset.top + 80)) {
            nav.classList.add('nav__scroll')
        } else {
            nav.classList.remove('nav__scroll')
        }
    };
});