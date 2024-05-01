// This block is executed after the DOM has fully loaded.
document.addEventListener('DOMContentLoaded', function () {
    // Selects the element intended to toggle the collapse functionality.
    var collapser = document.querySelector('[data-toggle="collapse"]');
    // Fetches the icon within the collapser element.
    var icon = collapser.querySelector('i');
    
    // Adds a click event listener to the collapser to handle the toggle of icons.
    collapser.addEventListener('click', function () {
        // Check if the icon currently shows a "down" chevron to switch to "up".
        if (icon.classList.contains('fa-chevron-down')) {
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-up');
        } else {
            // Otherwise, switch from "up" chevron back to "down".
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
        }
    });
});

// This block ensures the Masonry layout is correctly applied after images have loaded.
document.addEventListener('DOMContentLoaded', function () {
    // Selects the container that holds product cards.
    var elem = document.querySelector('.products-container');
    // Collects all image elements within the container.
    var images = elem.getElementsByTagName('img');
    var totalImages = images.length;
    var imagesLoaded = 0;

    // Initializes the Masonry layout with specified options.
    var msnry = new Masonry(elem, {
        itemSelector: '.product-card',  // Selects which elements are considered as items.
        columnWidth: '.product-card',  // Defines the width of columns based on a product card.
        percentPosition: true,         // Positions items by percentage to reduce gaps.
        gutter: 10,                    // Sets space between items.
        fitWidth: true,                // Centers the grid inside the container.
        horizontalOrder: true          // Keeps a left-to-right order in multi-row layouts.
    });

    // Function to track each image load.
    function imageLoaded() {
        imagesLoaded++;
        if (imagesLoaded === totalImages) {
            // When all images are loaded, recalculate the layout.
            msnry.layout();
        }
    }

    // Check each image if it has already completed loading.
    for (var i = 0; i < totalImages; i++) {
        if (images[i].complete) {
            imageLoaded();  // If already loaded, invoke the layout function.
        } else {
            // Otherwise, attach load and error events to trigger the layout function.
            images[i].addEventListener('load', imageLoaded);
            images[i].addEventListener('error', imageLoaded);
        }
    }

    // If there are no images, immediately layout Masonry as there's nothing to wait on.
    if (totalImages === 0) {
        msnry.layout();
    }
});

// This block is responsible for handling form submission via a span element.
document.addEventListener('DOMContentLoaded', function() {
    // Finds the span and form based on their IDs.
    var submitSpan = document.getElementById('submitPrice');
    var form = document.getElementById('priceForm');

    // Checks if both elements exist.
    if (submitSpan && form) {
        // Adds click event to the span that submits the form.
        submitSpan.addEventListener('click', function() {
            form.submit();  // Triggers form submission.
        });
    } else {
        // Logs an error if the necessary elements are not found.
        console.error('Elements not found');
    }
});
