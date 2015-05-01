
// Code to populate a conversation when one is clicked
var current_convo = "";
var lastSender = "";
var getName = {};
var convo_user = "";
var convo_name = "";
var convo_id = "";

function addMessage(message) {
    "use strict";
    if(lastSender !== message[2]){
        lastSender = message[2];
        $("#messages").append('<div class="message"><div class="message-header"><div class="commenterImage"><img src="../media/avatars/' + getName[lastSender + "_user"] + '.jpg"></div>' + getName[lastSender].trim() + ':</div></div>');
    }
    $(".message").last().append('<div>' + message[1] + '</div>');
    $('#messages').scrollTop($('#messages')[0].scrollHeight);
}

var populateConversation = function () {
    "use strict";
    current_convo = ""; lastSender = ""; getName = {};
    convo_user = $(this).val();
    convo_name = $(this).html();
    convo_id = $(this).attr('userID');
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
            var i;
            for(i = 0; i < messages.length; i++){
                addMessage(messages[i]);
            }
        }
    });
};


$( document ).ready(function() {
    "use strict";
    $(".convo-name").click(populateConversation);
    $("#message-send").click(function (){
        var message = [3001, $("#message-box").val(), parseInt(userID), parseInt(convo_id), "dumb", null];
        addMessage(message);
        $("#message-box").val('');
    });
    $("#message-box").keydown(function(event) {
        if (event.keyCode === 13) {
            $("#message-send").click();
            return false;
        }
    });
});
