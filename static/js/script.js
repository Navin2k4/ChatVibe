// For loading animation for the Pricing boxex

$(document).ready(function () {
    $(window).scroll(function () {
        $(".card").each(function () {
            var bottom_of_element = $(this).offset().top + $(this).outerHeight();
            var bottom_of_window = $(window).scrollTop() + $(window).height();

            if (bottom_of_window > bottom_of_element) {
                $(this).addClass("visible");
            }
        });
    });
});

// for carousel looping

$(document).ready(function () {
    $('#carouselExampleInterval').on('slid.bs.carousel', function (e) {
        var carousel = $(this);
        var slides = carousel.find('.carousel-item');
        var activeSlide = carousel.find('.carousel-item.active');
        var lastSlide = slides.last();
        if (activeSlide.index() === lastSlide.index()) {
            carousel.carousel('pause');
            setTimeout(function () {
                carousel.carousel(0);
                carousel.carousel('cycle');
            }, 1000);
        }
    });
});

// For using in the home.index to validate the username and the room name
function validateForm() {
    var roomName = document.getElementById("room_name").value;
    var username = document.getElementById("username").value;

    var alphaRegex = /^[A-Za-z\s]+$/;

    if (roomName.trim() === '' || username.trim() === '') {
        alert("Please fill in both Room Name and Username fields");
        return false;
    }

    if (!alphaRegex.test(roomName) || !alphaRegex.test(username)) {
        alert("No special characters such as '/._ are allowed. ");
        return false;
    }

    if (roomName.toLowerCase() === "admin" || username.toLowerCase() === "admin") {
        alert("Room name or username cannot be 'admin'. Please choose a different name.");
        return false;
    }

    return true;
}
