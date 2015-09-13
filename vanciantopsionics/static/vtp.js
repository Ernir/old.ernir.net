$(function () {
    //TODO refactor

    $("#statement-title").click(function () {
        var $body = $("#statement-body");
        var $title = $("#statement-title");
        if ($body.is(":hidden")) {
            $body.slideDown("slow");
            $title.html("<a href='#'>Read less (for normal people)</a>");
        }
        else {
            $body.slideUp("slow");
            $title.html("<a href='#'>Read more (for D&D fans)</a>");
        }
    });

    $("#faq-title").click(function () {
        var $body = $("#faq-body");
        var $title = $("#faq-title");
        if ($body.is(":hidden")) {
            $body.slideDown("slow");
            $title.html("<a href='#'>Hide FAQ</a>");
        }
        else {
            $body.slideUp("slow");
            $title.html("<a href='#'>The FAQ (also for D&D fans)</a>");
        }
    });
});

$("#toc").tocify({
    selectors: "h1,h2,h3,h4",
    hashGenerator: "pretty"
});