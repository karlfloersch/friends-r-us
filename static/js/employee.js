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
     // item_name, num_aval_units, unit_price, content, employee_id, type, date, company
    var data = {
        'item_name': $('#item_name').val(),
        'num_aval_units': $('#num_aval_units').val(),
        'unit_price': $('#unit_price').val(),
        'content': $('#content').val(),
        'type': $('#type').val(),
        'company': $('#company').val(),
        
    };
    sendDefaultPOST('/submit-comment/', data, function(response) {
        console.log(response);

        // in here, populate the shit
    });

};
// var hidesalesreport = function(){
// $.ajax({
//    /* ... other options here... */
//    success: function (){
//        $('#sales_table_values').hide();
//    }
// });


// };