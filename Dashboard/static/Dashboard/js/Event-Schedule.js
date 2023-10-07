$(document).ready(function() {
    const $pages = $(".page");
    const $backButton = $(".back");
    const $nextButton = $(".next");
    const pageSize = 5; // Set the number of visible pages
    let currentPage = 1; // Initialize the current page

    function navigatePage(targetPage) {
        const nextPage = $(targetPage);

        if (!nextPage.hasClass("disabled") && !nextPage.hasClass("active")) {
            $pages.removeClass("active");
            nextPage.addClass("active");
            currentPage = parseInt(nextPage.data("page"));

            updateButtonState();
        }
    }

    function updateButtonState() {
        const isFirstPage = currentPage === 1;
        const isLastPage = currentPage === $pages.length;

        $pages.removeClass("disabled");

        if (isFirstPage) {
            $backButton.addClass("disabled");
        } else {
            $backButton.removeClass("disabled");
        }

        if (isLastPage) {
            $nextButton.addClass("disabled");
        } else {
            $nextButton.removeClass("disabled");
        }
    }

    function updateVisiblePages() {
        $pages.addClass("d-none");

        const startPage = Math.max(currentPage - Math.floor(pageSize / 2), 1);
        const endPage = Math.min(startPage + pageSize - 1, $pages.length);

        for (let i = startPage; i <= endPage; i++) {
            $(`.page[data-page="${i}"]`).removeClass("d-none");
        }
    }

    $pages.on("click", function(e) {
        e.preventDefault();
        const targetPage = this;
        navigatePage(targetPage);
        updateVisiblePages(); // Update visible pages on click
    });

    $backButton.on("click", function(e) {
        e.preventDefault();
        if (!$(this).hasClass("disabled")) {
            const prevPage = currentPage - 1;
            if (prevPage >= 1) {
                navigatePage(`.page[data-page="${prevPage}"]`);
                updateVisiblePages();
            }
        }
    });

    $nextButton.on("click", function(e) {
        e.preventDefault();
        if (!$(this).hasClass("disabled")) {
            const nextPage = currentPage + 1;
            if (nextPage <= $pages.length) {
                navigatePage(`.page[data-page="${nextPage}"]`);
                updateVisiblePages();
            }
        }
    });

    // Initially set the first page as active
    navigatePage(`.page[data-page="1"]`);
    updateVisiblePages();
});
