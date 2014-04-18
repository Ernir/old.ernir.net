$(function () {

    $(".show-comments").click(function () {
        var $commentSection = $(this).parent().siblings(".comment-list");

        if ($commentSection.is(":hidden") && ($commentSection.children().length > 0 )) {
            $commentSection.slideDown("fast");
        } else if (!$commentSection.is(":hidden")) {
            $commentSection.slideUp("fast");
        }
    });
});