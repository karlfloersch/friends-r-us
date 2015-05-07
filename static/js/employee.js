var getsalesreport = function() {
    // get the month in jQuery -- $('#sales-month').val();
    // put month in data
    // call the correct url and fill out the success function
    var data = {
        'comment_text': comment,
        'post_id': $actionBox.attr('value')
    };
    sendDefaultPOST('/submit-comment/', data, function(response) {
        console.log(response);

        // in here, populate the shit
    });

};
var create_advertisement = function() {

    var data = {

        'item_name': $('#item_name').val(),
        'num_aval_units': $('#num_aval_units').val(),
        'unit_price': $('#unit_price').val(),
        'content': $('#content').val(),
        'type': $('#type').val(),
        'company': $('#company').val(),
        // 'date': today 

    };
    sendDefaultPOST('/create-advertisement/', data, function(response) {
        console.log(response);
    });

};

var get_all_advertisment = function() {
    $('#advertisement-list').toggle()
    var data = {

    };
    sendDefaultPOST('/produce-list-of-all-items-advertised/', data, function(response) {
        console.log(response.items);
        var i;
        $('#advertisement-list').append('<tr><td>' + "advertisement ID" + '</td><td>' + "item name" + '</td><td>' + "unit price" + '</td><td>' + "num avaliable units" + '</td></tr>');
        $('#advertisement-list').find("tr:gt(0)").remove();
        for (i = 0; i < response.items.length; i++) {
            $('#advertisement-list').append('<tr><td>' + response.items[i][0] + '</td><td>' + response.items[i][1] + '</td><td>' + response.items[i][2] + '</td><td>' + response.items[i][3] + '</td><td class="delete-ad-list-row">Delete</td></tr>');
        }
        $('.delete-ad-list-row').click(function() {
            var id = $(this).parent().children('td').eq(0).text();
            $(this).parent().remove();

            var data = {
                'id': id
            };
            sendDefaultPOST('/delete-advertisement/', data, function(response) {
                console.log(response);


                // in here, populate the shit
            });


        });


    });

};
var delete_advertisement = function() {

    var data = {

    };
    sendDefaultPOST('/delete-advertisement/', data, function(response) {
        console.log(response);
    });

};
var generate_mailing_list = function() {
    $('#mailing-list').toggle()
    var data = {

    };

    sendDefaultPOST('/generate-mailing-list/', data, function(response) {
        // console.log(response);
        // mailing-list

         var i;
        $('#mailing-list').append('<tr><td>' + "Email" + '</td></tr>');
        $('#mailing-list').find("tr:gt(0)").remove();
        for (i = 0; i < response.items.length; i++) {
            $('#mailing-list').append('<tr><td>' + response.items[i][0] + '</td></tr>');
        }
        
    });

};


$(document).ready(function() {
    "use strict";
    $("#create-advertisement").click(create_advertisement);
    $("#delete-advertisement").click(create_advertisement);
    $("#produce-list-of-all-items-advertised").click(get_all_advertisment);
    $("#generate-mailing-list").click(generate_mailing_list);
});