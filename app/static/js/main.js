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


	var newWords = [];
	$("#skillsform-skills").on({
		keyup: function(e){
			if(e.which==188 || e.which == 13) {
				//console.log($("#skillsform-skills").val());
				skillToAdd = $("#skillsform-skills").val();
				skillToAdd = skillToAdd.substring(0, skillToAdd.length - 1);

				var el = ("<li>" + skillToAdd + "</li>");
				$(".list-skills").append(el);
				//el.addClass("btn btn-primary btn-xs");

				$("#skillsform-skills").val('');
			}
		}
	});

	$("#learn-more").click(function(){
		target = $("#selling-point-one");

		$('html, body').animate({
          scrollTop: $(window).height() - $("nav").height()
        }, 1000);
	})
});