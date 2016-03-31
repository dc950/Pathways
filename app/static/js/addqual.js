$(document).ready(function() {

    $.ajax({
        method: "GET",
        data: {qual_id: 1},
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function (data) {
            $("#subjects").empty();
            $.each(data, function (value, key) {
                $("#subjects").append($("<option></option>").attr("value", parseInt(value)).text(key));
            });
        }
    })
});
