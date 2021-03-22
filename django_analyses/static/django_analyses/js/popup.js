$(document).ready(function () {
    $(".openpop").click(function (e) {
        e.preventDefault();
        Window.open($(this).attr('href'));
    });
});
