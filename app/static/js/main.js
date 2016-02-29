$(document).ready(function(){

	console.log("Pathways main.js loaded");

	$("#qualification_type").change(function() {
		console.log("qualification_type has been changed");
		console.log(this.value);

		$.ajax({
		  	method: "GET",
		  	data: { qual_id: this.value },
		  	dataType: 'json',
          	contentType: 'application/json; charset=utf-8',
          	success: function (data) {
            	console.log(data);

            	$("#subjects").empty();
            	$.each(data, function(value, key){
            		$("#subjects").append($("<option></option>").attr("value", parseInt(value)).text(key));
            	});
        	}
		})
	});

	$("#learn-more").click(function(){
		target = $("#selling-point-one");

		$('html, body').animate({
          scrollTop: $(window).height() - $("nav").height()
        }, 1000);
	})
});