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
var list_all_employees = function(){
// list_all_customers_ajax
    // ('#employee_table').toggle()
    var data = {
    };
    sendDefaultPOST('/list-all-employees/', data, function(response) {
        $('#employee_table').toggle();
        var i;
        $('#employee_table').append('<tr><td>' + "firstname" +'</td><td>' + "lastname" + '</td><td>'+"gender"+'</td><td>'+"address"+'</td><td>'+"city"+'</td><td>'+"state"+'</td><td>'+"zipcode"+'</td><td>'+"telephone"+'</td><td>'+"SSN"+'</td><td>'+"hourly rate"+'</td><td>'+"role"+'</td><td>'+"ID"+'</td><td>'+ '</td></tr>');
        $('#employee_table').find("tr:gt(0)").remove();
        // console.log("bobs");
        for (i = 0; i < response.items.length; i++) {
            var j;
            var strings = '<tr><td>'
            // console.log('bob');
            for(j = 0 ; j<response.items[i].length; j++){
                if(j==response.items[i].length-1){
                    strings = strings + response.items[i][j];
                }else{
                    strings = strings + response.items[i][j] + '</td><td>';
                }
            }
            strings = strings +'</td><td class="update-cust-list-row">Update' +'</td><td class="delete-cust-list-row">Delete'+ '</td></tr>'
            // console.log(strings);
            $('#employee_table').append(strings);
        }



        $('.update-cust-list-row').click(function() {
            array_to_store =[]
            var i;
            console.log("hello")
            for(i=0; i <14; i++){
                array_to_store[i] = $(this).parent().children('td').eq(i).text();
                // console.log($(this).parent().children('td').eq(i).text());
            }
            console.log(array_to_store);
            var data = {
                'ar': array_to_store
            };
            console.log("we wanna be here");
             sendDefaultPOST('/update-employee/', data, function(response) {
                console.log(response);
            });

        });
        $('.delete-cust-list-row').click(function() {
            var id = $(this).parent().children('td').eq(11).text();
            $(this).parent().remove();

            var data = {
                'id': id
            };
            sendDefaultPOST('/delete-employee/', data, function(response) {
                console.log(response);
            });
        });


       $(function () {
    $("#employee_table td:not(:nth-child(11) , :nth-child(12), :nth-child(13))").click(function (e) {
        e.preventDefault(); // <-- consume event
        e.stopImmediatePropagation();

        $this = $(this);

        if ($this.data('editing')) return;  

        var val = $this.text();

        $this.empty()
        $this.data('editing', true);        

        $('<input type="text" class="editfield">').val(val).appendTo($this);
    });

    putOldValueBack = function () {
        $("#employee_table .editfield").each(function(){
            $this = $(this);
            var val = $this.val();
            var $td = $this.closest('td');
            $td.empty().html(val);
            $td.data('editing', false);

        });
    }

    $(document).click(function (e) {
        putOldValueBack();
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
    $("#list-all-employees").click(list_all_employees);
});
