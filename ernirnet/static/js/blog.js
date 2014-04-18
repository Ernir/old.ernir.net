$(function () {

    $(".show-comments").click(function () {
        var $commentSection = $(this).parent().siblings(".comment-section");

        if ($commentSection.is(":hidden") && ($commentSection.children(".comment-list").length > 0 )) {
            $commentSection.slideDown("fast");
        } else if (!$commentSection.is(":hidden")) {
            $commentSection.slideUp("fast");
        }
    });
});