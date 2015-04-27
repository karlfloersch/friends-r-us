$( document ).ready(function() {
    "use strict";
    $(".comment-add").click(function() {
        var $actionBox = $(this).parent().parent().parent();
        var $commentBox = $actionBox.find(".comment-box");
        var comment = $commentBox.val();
        if (comment === ""){
            return;
        }
        $commentBox.val('');
        var hostname = $('<a>').prop('href', url).prop('hostname');
        var url = hostname + username;
        $actionBox.find(".commentList").append('<li> <div class="commenterImage"> <img src="../../media/avatars/' + username + '.jpg"> </div> <div class="commentText"> <p class="">' + comment + '</p> <span class="date sub-text">' + fullname + ', on ' + today + '</span> </div> </li>');
    });

});
