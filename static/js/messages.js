$( document ).ready(function() {
    "use strict";
    $(".convo-name").click(function (){
        var convo_user = $(this).val();
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
                console.log(response);
                var messages = response.messages;
                var i;
                for(i = 0; i < messages.length; i++){
                    $("#messages").append('<div class="message">' + messages[i][1] + '</div>');
                }
            }
        });
    });
});
