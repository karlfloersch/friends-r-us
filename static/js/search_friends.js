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
    element.autocomplete({
        minLength: 0,
        source: values,
        focus: function( event, ui ) {
            element.val( ui.item.label );
            return false;
        }
    });
    element.data( "ui-autocomplete" )._renderItem = function( ul, item ) {
        var $li = $('<li>'),
            $imgContainer = $('<div>'),
            $img = $('<img>'),
            url = getBaseURL();
        $img.attr({
          src: url + 'media/avatars/' + item.username + '.jpg',
        });
        $li.attr('data-value', item.label);
        $imgContainer.addClass('commenterImage');
        $imgContainer.append($img);
        $li.append('<a href="' + url + 'accounts/' + item.username + '">');
        $li.find('a').append($imgContainer).append(item.label);    
        return $li.appendTo(ul);
    };
}
var searchFriends = function (redirect) {
    "use strict";
    var textValue = $('#page-search').val();
    if(textValue.slice(-1) !== " " && !redirect){
        return;
    }
    var name = textValue.trim().split(" ");
    var firstName = name[0];
    // Create URL
    var urlSubmit = getBaseURL() + "get_friends/";
    var data ={
        "name": firstName.split(" ")[0]
    };
    $.ajax({
        type: "POST",
        url: urlSubmit,
        dataType: "json",
        data : data,
        success: function(response){
            var friends = [];//JSON.parse(response);
            var bestGuess = 0;
            var i = 0;
            for(i = 0; i < response.friends.length; i++){
                if(redirect){
                    // If we are redirecting try to see if we can
                    // match the last name with what was provided 
                    if(name.length !== 1){
                        if(name[1] === response.friends[i][2]){
                            bestGuess = i;
                        }
                    }
                }
                friends.push({'label': response.friends[i][1] + ' ' +
                              response.friends[i][2],
                              'value': response.friends[i][1] + ' ' +
                              response.friends[i][2],
                              'username': response.friends[i][3]});
            }
            // If we are redirecting (when search button pressed)
            // then use our best guess on who this is searching for
            // and go to their page
            if(redirect){
                window.location.href = getBaseURL() + 'accounts/' + response.friends[bestGuess][3];
            }
            addAutoComplete($("#page-search"), friends);
        }
    });
};

$( document ).ready(function() {
    "use strict";
    $('#page-search').keyup(function(event) {
        if(event.keyCode === 13){
            return searchFriends(true);
        }
        return searchFriends(false);
    });

    $('#page-search-submit').click(function() {
        return searchFriends(true);
    });
});
