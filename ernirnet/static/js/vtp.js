$(function () {
    $("#reveal-statement").click(function () {
        var $statement = $("#statement");
        var $revealButton = $("#reveal-statement");
        if ($statement.is(":hidden")) {
            $statement.slideDown("slow");
            $revealButton.text("Read less (for normal people)");
        }
        else {
            $statement.slideUp("slow");
            $revealButton.text("Read more (for D&D fans)");
        }
    })
});