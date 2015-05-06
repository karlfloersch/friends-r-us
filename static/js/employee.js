var getsalesreport = function() {

    var data = {
        'comment_text': comment,
        'post_id': $actionBox.attr('value')
    };
    sendDefaultPOST('/submit-comment/', data, function(response) {
        console.log(response);
    });

};

var hidesalesreport = function(){
$.ajax({
   /* ... other options here... */
   success: function (){
       $('#sales_table_values').hide();
   }
});


};