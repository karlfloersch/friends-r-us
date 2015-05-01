function getBaseURL() {
    "use strict";
    var url = location.href;  // entire url including querystring - also: window.location.href;
    var baseURL = url.substring(0, url.indexOf('/', 14));
    if (baseURL.indexOf('http://localhost') !== -1) {
        // Base Url for localhost
        url = location.href;  // window.location.href;
        var pathname = location.pathname;  // window.location.pathname;
        var index1 = url.indexOf(pathname);
        var index2 = url.indexOf("/", index1 + 1);
        var baseLocalUrl = url.substr(0, index2);

        return baseLocalUrl + "/";
    }
    else {
        // Root Url for domain name
        return baseURL + "/";
    }
}

function addAutoComplete(element, values) {
    "use strict";
            console.log(values);
    element.autocomplete({
        source: values
    });
}

var searchFriends = function () {
    "use strict";
    var textValue = $('#page-search').val();
    if(textValue.slice(-1) !== " "){
        return;
    }
    var firstName = textValue.trim();
    // Create URL
    var urlSubmit = getBaseURL() + "get_friends/";
    var data ={
        "name": firstName
    };
    $.ajax({
        type: "POST",
        url: urlSubmit,
        dataType: "json",
        data : data,
        success: function(response){
            var friends = [];//JSON.parse(response);
            var i = 0;
            for(i = 0; i < response.friends.length; i++){
                friends.push(response.friends[i][1] + " " +
                             response.friends[i][2]);
            }
            addAutoComplete($("#page-search"), friends);
        }
    });
};

$( document ).ready(function() {
    "use strict";
    $('#page-search').keyup(searchFriends);
});
