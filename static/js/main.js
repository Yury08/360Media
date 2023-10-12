window.addEventListener('scroll', function () {
    let header = document.querySelector("header");
    header.classList.toggle("fixed", window.scrollY > 0);
})

// search
const search = document.querySelector('#search-icon')
const search_input = document.querySelector('#search-input')
const search_button = document.querySelector('#search-btn')
search.addEventListener('click', function () {
    search_input.classList.toggle('search__input-active')
    search_input.classList.toggle('search__input')
    // button
    search_button.classList.toggle('search-btn')
    search_button.classList.toggle('search-btn-active')
})

//burger
const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-link');
    const navLink = document.querySelectorAll('.nav-link a')

    burger.addEventListener('click', () => {
        //canvas
        nav.classList.toggle('burger-active');
        nav.classList.toggle('close-burger');

        //links
        navLink.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = '';
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + .3}s`;
            }
        });
        // burger animation
        burger.classList.toggle('toggle')
    });
};

navSlide()

const r = document.querySelector('form[name=rating]');

r.addEventListener("change", function (e) {
    // Получаем данные из формы
    e.preventDefault();
    let d = new FormData(this);
    fetch(`${this.action}`, {
        method: 'POST',
        body: d
    })
        .then(response => alert("Рейтинг установлен"))
        .catch(error => alert("Ошибка"))
});

$(document).ready(function () {
    // like
    $(`a.comm__like`).on("click", function (e) {
        console.log("click");
        $.ajax('http://127.0.0.1:5000/reaction/',{
            url: 'http://127.0.0.1:5000/reaction/',
            data: {
                "action": $(this).data("action"),
                "rev_id": $(this).data("id"),
            },
            success: function() {
                location.reload();
            }
        })
    })

    // dislike
    // $(`#reaction-dislike`).on("click", function (e) {
    //     console.log("DISLIKE");
    //     $.ajax("http://127.0.0.1:5000/reaction/", {
    //         method: "GET",
    //         url: "http://127.0.0.1:5000/reaction/",
    //         data: {
    //             "action": $(this).data("action"),
    //             "rev_id": $(this).data("id"),
    //         },
    //         success: function() {
    //             location.reload();
    //         }
    //     })
    // })
})
