$(function () {
    //TODO refactor

    $(".delete-comment-button").click(function () {
        var $button = $(this);
        flash_warning($button);
        setTimeout(function(){remove_warning($button);},800);
    });

    $(".delete-comment-button").dblclick(function(){
        var $row = $(this).closest("tr");
        var id = $row.attr("id").slice(4);
        $.post("/admin/delete/comment/", {id : id});
        $row.remove();
    })
});

function flash_warning($theButton){
    $theButton.removeClass("btn-warning").addClass("btn-danger");
}

function remove_warning($theButton){
    $theButton.removeClass("btn-danger").addClass("btn-warning");
}