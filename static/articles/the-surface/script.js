// Select all elements with the class 'content'
const elements = document.querySelectorAll('.content');

// Add event listeners to each element
elements.forEach(element => {
    // Add class on mouseenter (hover)
    element.addEventListener('mouseenter', () => {
        element.classList.remove('rotate-back');
        element.classList.add('rotate');
    });

    // Remove class on mouseleave (unhover)
    element.addEventListener('mouseleave', () => {
        element.classList.remove('rotate');
        element.classList.add('rotate-back');
    });
});

let content = document.querySelector('#content');
content.addEventListener('click', () => {
    if (content.querySelector('.img').classList.contains('rotate90-down')){
        content.querySelector('.img').classList.remove('rotate90-down');
        document.querySelector('#data').classList.remove('fade-down');
        document.querySelector('#data').classList.add('fade-up');
        setTimeout(() => {
            document.querySelector('#data').style.display = "none";
        }, 500);
    } else {
        content.querySelector('.img').classList.add('rotate90-down');
        document.querySelector('#data').style.display = "flex";
        document.querySelector('#data').classList.remove('fade-up');
        document.querySelector('#data').classList.add('fade-down');
    }
})