"use strict";

document.addEventListener('DOMContentLoaded', function() {
    function adjustContentMargin() {

        let totalFlashMessageHeight = 0;
        const flashMessages = document.querySelectorAll('#flashMessages .alert');

        flashMessages.forEach(function(message) {
            totalFlashMessageHeight += message.offsetHeight;
        });


        const content = document.querySelector('.content');
        content.style.marginTop = (100 + totalFlashMessageHeight) + 'px';
    }

    adjustContentMargin();

    document.querySelectorAll('#flashMessages .alert .close').forEach(function(button) {
        button.addEventListener('click', function() {
            const alert = this.closest('.alert');
            alert.classList.remove('show');
            alert.addEventListener('transitionend', function() {
                alert.remove();
                adjustContentMargin();
            });
        });
    });
});
