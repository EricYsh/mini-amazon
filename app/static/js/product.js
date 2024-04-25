document.addEventListener('DOMContentLoaded', function () {
    var collapser = document.querySelector('[data-toggle="collapse"]');
    var icon = collapser.querySelector('i');

    collapser.addEventListener('click', function () {
        if (icon.classList.contains('fa-chevron-down')) {
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-up');
        } else {
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var elem = document.querySelector('.products-container');
    var images = elem.getElementsByTagName('img');
    var totalImages = images.length;
    var imagesLoaded = 0;

    var msnry = new Masonry(elem, {
        itemSelector: '.product-card',
        columnWidth: '.product-card',
        percentPosition: true,
        gutter: 10,
        fitWidth: true,
        horizontalOrder: true
    });

    function imageLoaded() {
        imagesLoaded++;
        if (imagesLoaded === totalImages) {
            msnry.layout();
        }
    }

    for (var i = 0; i < totalImages; i++) {
        if (images[i].complete) {
            imageLoaded();  
        } else {
            images[i].addEventListener('load', imageLoaded);
            images[i].addEventListener('error', imageLoaded); 
        }
    }

    if (totalImages === 0) {
        msnry.layout();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var submitSpan = document.getElementById('submitPrice');
    var form = document.getElementById('priceForm');

    if (submitSpan && form) {
        submitSpan.addEventListener('click', function() {
            form.submit();
        });
    } else {
        console.error('Elements not found');
    }
});
