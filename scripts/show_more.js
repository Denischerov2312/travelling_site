const showMore = document.querySelector('.button__show-more');
const tourLength =  document.querySelectorAll('.tour').length;
let items = 15;


function check_button() {
    if ( items > tourLength ) {
        showMore.style.display = 'none';
    }
}

check_button()

showMore.addEventListener('click', () => {
    items += 10
    const array = Array.from(document.querySelector('.main__tours').children);
    const visItems = array.slice(0, items)

    visItems.forEach(el => el.classList.add('is-visible'));

    if (visItems.length === tourLength) {
        showMore.style.display = 'none';
    }
});