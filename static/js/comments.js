var commentClick = function() {
    "use strict";
    var $actionBox = $(this).parent().parent().parent().parent();
    var $commentBox = $actionBox.find(".comment-box");
    var comment = $commentBox.val();
    var numLikes = 5;
    if (comment === ""){
        return;
    }
    $commentBox.val('');
    var hostname = $('<a>').prop('href', url).prop('hostname');
    var url = hostname + username;
    $actionBox.find(".commentList").append('<li> <div class="commenterImage"> <img src="../../media/avatars/' + username + '.jpg"> </div> <div class="commentText"> <p class="">' + comment + '</p> <span class="date sub-text">' + numLikes + ' Likes - <a href="#">Like</a><br>' + fullname + ', on ' + today + '</span> </div> </li>');
};

$( document ).ready(function() {
    "use strict";
    $(".comment-add").click(commentClick);

    $("#post-add").click(function() {
        var $posts = $("#posts");
        var post = $("#post-box").val();
        if (post === ""){
            return;
        }
        $("#post-box").val('');
        var hostname = $('<a>').prop('href', url).prop('hostname');
        var url = hostname + username;
        $posts.prepend('<div class="detailBox"><div class="titleBox"><div class="commenterImage"> <img src="../../media/avatars/' + username + '.jpg"> </div><label>' + fullname + '</label></div><div class="commentBox"><p class="taskDescription">' + post + '</p></div><div class="actionBox"><ul class="commentList"></ul><form role="form"><div class="row"><div class="col-md-10"><textarea rows="1" cols="40" class="form-control comment-box" type="text" placeholder="Write a comment..."></textarea></div><div class="col-md-2"><button type="button" class="btn btn-default comment-add">Add</button></div></div></form></div></div>');
        $(".comment-add").click(commentClick);
    });

});


