// Wrapper function for sending POST requests.
var sendPOST = function(url, data, onSuccess){
    "use strict";
    var getUrl = window.location;
    var baseUrl = getUrl .protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];
    var urlSubmit = baseUrl + url;
    $.ajax({
        type: "POST",
        url: urlSubmit,
        dataType: "json",
        data : data,
        success: onSuccess
    });
};

var sendDefaultPOST = function(url, data, onSuccess){
    "use strict";
    var userInfo = {
        'username': username,
        'userID': userID,
        'fullname': fullname
    };
    data = $.extend(data, userInfo);
    sendPOST(url, data, onSuccess); 
};

// Setup stuff for the CSRF Token/post requests
// using jQuery. Code supplied from Django
// and can be found here: https://docs.djangoproject.com/en/1.8/ref/csrf/
function getCookie(name) {
    "use strict";
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    "use strict";
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        "use strict";
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
