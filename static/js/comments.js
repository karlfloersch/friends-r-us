var addComment = function() {
    "use strict";
    var $actionBox = $(this).parent().parent().parent().parent();
    var $commentBox = $actionBox.find(".comment-box");
    var comment = $commentBox.val();
    var numLikes = 5;
    if (comment === ""){
        return;
    }
    $commentBox.val('');
    $actionBox.find(".commentList").append('<li> <div class="commenterImage"> <img src="../../media/avatars/' + username + '.jpg"> </div> <div class="commentText"> <p class="">' + comment + '</p> <span class="date sub-text">' + numLikes + ' Likes - <a href="#">Like</a><br>' + fullname + ', on ' + today + '</span> </div> </li>');
    $('.commentList').scrollTop($('.commentList')[0].scrollHeight);
};

var addPost = function() {
    "use strict";
    var $posts = $("#posts");
    var post = $("#post-box").val();
    var data = {
        'post_text': post,
        'page_name': $('#circle-name').attr('value'),
        'circle_id': $('#circle-id').attr('value')
    };

    sendDefaultPOST('/submit-post/', data, function(response) {
        console.log(response);
    });
    $("#post-box").val('');
    $posts.prepend('<div class="detailBox"><div class="titleBox"><div class="commenterImage"> <img src="../../media/avatars/' + username + '.jpg"> </div><label>' + fullname + '</label></div><div class="commentBox"><p class="taskDescription">' + post + '</p></div><div class="actionBox"><ul class="commentList"></ul><form role="form"><div class="row"><div class="col-md-10"><textarea rows="1" cols="40" class="form-control comment-box" type="text" placeholder="Write a comment..."></textarea></div><div class="col-md-2"><button type="button" class="btn btn-default comment-add">Add</button></div></div></form></div></div>');
    $(".comment-add").click(addComment);
    enableSubmitOnEnter();
};

function enableSubmitOnEnter() {
    "use strict";
    $(".comment-box").keydown(function(event) {
        if (event.keyCode === 13) {
            $(".comment-add").click();
            return false;
        }
    });
}

$( document ).ready(function() {
    "use strict";
    $(".comment-add").click(addComment);
    enableSubmitOnEnter();

    $("#post-add").click(addPost);

});


