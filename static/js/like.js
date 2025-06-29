const like = document.getElementById('like');

like.addEventListener('click', function (e) {
    e.preventDefault();

    const isLiked = like.classList.contains('liked');

    if (isLiked) {
        like.src = like.dataset.off;
        like.classList.remove('liked');
    } else {
        like.src = like.dataset.on;
        like.classList.add('liked');
    }
});