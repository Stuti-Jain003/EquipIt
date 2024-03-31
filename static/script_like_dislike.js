$(document).ready(function () {
    $('#like-form').submit(function (event) {
        event.preventDefault();
        $.post($(this).attr('action'), function (data) {
            $('#like-count').text(data.likes + ' 👍');
        });
    });

    $('#dislike-form').submit(function (event) {
        event.preventDefault();
        $.post($(this).attr('action'), function (data) {
            $('#dislike-count').text(data.dislikes + ' 👎');
        });
    });
});