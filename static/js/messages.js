var current_convo = "";

$( document ).ready(function() {
    "use strict";
    $(".convo-name").click(function (){
        var convo_user = $(this).val();
        var convo_name = $(this).html();
        var convo_id = $(this).attr('userID');
        var getName = {};
        getName[userID.toString()] = fullname;
        getName[convo_id.toString()] = convo_name;
        getName[userID.toString() + "_user"] = username;
        getName[convo_id.toString() + "_user"] = convo_user;
        $("#new-message").show();
        if(convo_user.localeCompare(current_convo) === 0){
            return;
        }
        current_convo = convo_user;
        // Create URL
        var getUrl = window.location;
        var baseUrl = getUrl .protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];
        var urlSubmit = baseUrl + "/get_messages/";
        var data ={
            "convo_user": convo_user
        };
        $.ajax({
            type: "POST",
            url: urlSubmit,
            dataType: "json",
            data : data,
            success: function(response){
                var messages = response.messages;
                var lastSender = "";
                var i;
                for(i = 0; i < messages.length; i++){
                    if(lastSender !== messages[i][2]){
                        lastSender = messages[i][2];
                        $("#messages").append('<div class="message"><div class="message-header"><div class="commenterImage"><img src="../media/avatars/' + getName[lastSender + "_user"] + '.jpg"></div>' + getName[lastSender].trim() + ':</div></div>');
                    }
                    $(".message").last().append('<div>' + messages[i][1] + '</div>');
                }
            }
        });
    });
});
