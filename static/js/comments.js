var addComment = function() {
    "use strict";
    var $actionBox = $(this).parent().parent().parent().parent();
    var $commentBox = $actionBox.find(".comment-box");
    var comment = $commentBox.val();
    var numLikes = 0;
    if (comment === ""){
        return;
    }
    var data = {
        'comment_text': comment,
        'post_id': $actionBox.attr('value')
    };
    sendDefaultPOST('/submit-comment/', data, function(response) {
        console.log(response);
    });
    $commentBox.val('');
    $actionBox.find(".commentList").append('<li> <div class="commenterImage"> <img src="../../media/avatars/' + username + '.jpg"> </div> <div class="commentText"> <p class="">' + comment + '</p> <span class="date sub-text">' + numLikes + ' Likes - <a href="#">Like</a><br>' + fullname + ', on ' + today + '</span> </div> </li>');
    $('.commentList').scrollTop($('.commentList')[0].scrollHeight);
};

var purchase= function(){
    var data = {
        'item_id_input':$('#item_id_input').val(),
        'quantity_input':$('#quantity_input').val()
    };
        sendDefaultPOST('/purchase-item/', data, function(response) {
        console.log(response);
    });
};
var addPost = function() {
    "use strict";
    var $posts = $("#posts");
    var post = $("#post-box").val();
    var numLikes = 0;
    var data = {
        'post_text': post,
        'page_name': $('#circle-name').attr('value'),
        'circle_id': $('#circle-id').attr('value')
    };
    sendDefaultPOST('/submit-post/', data, function(response) {
        console.log(response);
    });
    $("#post-box").val('');
    $posts.prepend('<div class="detailBox"><div class="titleBox"><div class="commenterImage"> <img src="../../media/avatars/' + username + '.jpg"> </div><label>' + fullname + '</label><div class="date sub-text">' + numLikes + ' Likes - <a href="#">Like</a><br>' + fullname + ', on ' + today + '</div></div><div class="commentBox"><p class="taskDescription">' + post + '</p></div><div class="actionBox"><ul class="commentList"></ul><form role="form"><div class="row"><div class="col-md-10"><textarea rows="1" cols="40" class="form-control comment-box" type="text" placeholder="Write a comment..."></textarea></div><div class="col-md-2"><button type="button" class="btn btn-default comment-add">Add</button></div></div></form></div></div>');
    $(".comment-add").click(addComment);
    enableSubmitOnEnter();
};

var toggleLikePost = function() {
    "use strict";
    var data;
    if($(this).text().localeCompare('Like') === 0){
        $(this).text('Unlike');
        data = {
            'like_type': 'like',
            'text_type': 'post',
            'post_id': $(this).attr('postID')
        };
        console.log();
        var current_likes = parseInt($($(this).parent().find('.num-likes').get(0)).text());
        $($(this).parent().find('.num-likes').get(0)).text(String(current_likes + 1));
        sendDefaultPOST('/submit-like/', data, function(response) {
        });
    }else if($(this).text().localeCompare('Unlike') === 0) {
        $(this).text('Like');
        console.log($(this).text());
        data = {
            'like_type': 'unlike',
            'text_type': 'post',
            'post_id': $(this).attr('postID')
        };
        var current_likes = parseInt($($(this).parent().find('.num-likes').get(0)).text());
        $($(this).parent().find('.num-likes').get(0)).text(String(current_likes - 1));
        sendDefaultPOST('/submit-like/', data, function(response) {
            console.log(response);
        });
    }
};


var toggleLikeComment = function() {
    "use strict";
    var data;
    if($(this).text().localeCompare('Like') === 0){
        $(this).text('Unlike');
        data = {
            'like_type': 'like',
            'text_type': 'comment',
            'post_id': $(this).attr('commentID')
        };
        sendDefaultPOST('/submit-like/', data, function(response) {
            console.log(response);
        });
    }else if($(this).text().localeCompare('Unlike') === 0) {
        $(this).text('Like');
        console.log($(this).text());
        data = {
            'like_type': 'unlike',
            'text_type': 'comment',
            'post_id': $(this).attr('commentID')
        };
        sendDefaultPOST('/submit-like/', data, function(response) {
            console.log(response);
        });
    }
};

function enableSubmitOnEnter() {
    "use strict";
    $(".comment-box").keydown(function(event) {
        if (event.keyCode === 13) {
            var $commentAdd = $(this).parent().parent().find('.comment-add');
            $commentAdd.click();
            return false;
        }
    });
}

$( document ).ready(function() {
    "use strict";
    $(".comment-add").click(addComment);
    enableSubmitOnEnter();
    $("#post-add").click(addPost);
    $('.like-post').click(toggleLikePost);
    $('.like-comment').click(toggleLikeComment);
    $('#list_item_suggestions').click(purchase);

});


