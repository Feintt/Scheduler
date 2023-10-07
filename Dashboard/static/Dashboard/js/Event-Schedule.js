$(document).ready(function() {
    // Cache frequently used selectors
    var $pages = $(".page");
    var $backButton = $(".back");
    var $nextButton = $(".next");

    // Function to handle page navigation
    function navigatePage(targetPage) {
        var activePage = $pages.filter(".active");
        var nextPage = $(targetPage);

        if (!nextPage.hasClass("disabled") && !nextPage.hasClass("active")) {
            activePage.removeClass("active");
            nextPage.addClass("active");

            // Enable or disable the "forward" and "back" buttons
            updateButtonState();
        }
    }

    // Function to update button state
    function updateButtonState() {
        var activePage = $pages.filter(".active");
        var isFirstPage = activePage.prev(".page:not(.disabled)").length === 0;
        var isLastPage = activePage.next(".page:not(.disabled)").length === 0;

        // Enable or disable the "back" button
        if (isFirstPage) {
            $backButton.addClass("disabled");
        } else {
            $backButton.removeClass("disabled");
        }

        // Enable or disable the "forward" button
        if (isLastPage) {
            $nextButton.addClass("disabled");
        } else {
            $nextButton.removeClass("disabled");
        }
    }

    // Click event handler for page links
    $pages.on("click", function(e) {
        e.preventDefault();
        var targetPage = this;
        navigatePage(targetPage);
    });

    // Click event handler for the "back" button
    $backButton.on("click", function(e) {
        e.preventDefault();
        var activePage = $pages.filter(".active");
        var prevPage = activePage.prev(".page:not(.disabled)");
        if (prevPage.length) {
            navigatePage(prevPage);
        }
    });

    // Click event handler for the "forward" button
    $nextButton.on("click", function(e) {
        e.preventDefault();
        var activePage = $pages.filter(".active");
        var nextPage = activePage.next(".page:not(.disabled)");
        if (nextPage.length) {
            navigatePage(nextPage);
        }
    });
});
