$(document).ready(function(){

	var nav_offset = $("nav").height();

	var test = [1, 2, 3, 4, 5, 6];

	/*$.ajax({
		  	method: "GET",
		  	data: { request_json: 1 },
		  	dataType: 'json',
          	contentType: 'application/json; charset=utf-8',
          	success: function (data) {
            	console.log(data);
            	test = data;
        	}
		})*/

	//console.log(test);
	
	//treeJSON = d3.json("../static/js/data.json", function(error, treeData) {
	treeJSON = d3.json("?request_json=1", function(error, treeData) {
		console.log("Loading error: " + error);
		console.log(treeData);

		var viewerWidth = $("#pathway-container").width();
    	var viewerHeight = $("#pathway-container").height();

    	var marginWidth = 100;
    	var columnWidth;

    	var titleHeight = 30;

    	var baseSvg = d3.select("svg")
        baseSvg.attr("width", viewerWidth).attr("height", viewerHeight);

    	var tree = d3.layout.tree().size([viewerHeight, viewerWidth]);

		var j = 0;
		var newCircles = [];

		$.each(treeData, function(index, value){
    		//console.log(index);

    		var circles = baseSvg.selectAll('circle').data(value.subjects);

	        newCircles[j] = {qualification: index ,level: value.level, subjects: circles.enter()};
	        j++;			
    	});

    	//var noLevels = console.log("Length : " + newCircles.length);

    	/*
    	 * Draw Nodes on screen for every subject undertaken
    	 */
    	$.each(newCircles, function(index, value){
    		//console.log(index)

    		columnWidth = (viewerWidth - (2 * marginWidth)) / newCircles.length;

    		var xPos = (columnWidth * index) + marginWidth;
    		

    		baseSvg.append("rect").attr("x", xPos).attr("y", nav_offset).attr("width", columnWidth).attr("height", titleHeight)
    		.attr("fill", getLevelColour(value.level));

    		baseSvg.append("text").attr("dx", xPos).attr("dy", 20 +  + nav_offset).text(value.qualification);

    		console.log(value.subjects[0].length);

    		var yHeight;

    		value.subjects.append('circle').attr('cx', function(d, i){
				return xPos + (columnWidth / 2);
			}).attr('cy', function(d, i){
				var n = value.subjects[0].length;
				var edgeMargin = 60;

				var workingHeight = viewerHeight - titleHeight - (2 * edgeMargin) - nav_offset;

				if (n > 1) {
					var y = (workingHeight / (n-1)) * i + nav_offset;
				} else {
					var y = workingHeight / 2 + nav_offset;
				}

				return y + edgeMargin + titleHeight;
				//return titleHeight + ((i+1) * 40);
			}).attr('r', '10').attr('data-subject', function(d){
				return d.name;
			}).attr('data-qualification', function(){
				return value.qualification
			}).attr('data-level', function(){
				return value.level;
			}).attr('class', function(){
				return getLevelClass(value.level);
			}).attr('fill', getLevelColour(value.level))

			value.subjects.append('text').attr("dx", function(d, i){
				return xPos + (columnWidth / 2) + 20;
			}).attr("dy", function(d, i){
				var n = value.subjects[0].length;
				var edgeMargin = 60;

				var workingHeight = viewerHeight - titleHeight - (2 * edgeMargin) - nav_offset;

				if (n > 1) {
					var y = (workingHeight / (n-1)) * i + nav_offset;
				} else {
					var y = workingHeight / 2 + nav_offset;
				}
				
				return y + edgeMargin + titleHeight;
			}).text(function(d){
				return d.name;
			}).attr('class', 'node-label');
    	});

    	var toolTip;

    	/*
    	 * Draw ToolTips on screen when node is hovered over
    	 */
    	$(".node").on({	
			mouseenter : function(){
				var currentNode = $(this);
    			window.mytimeout = setTimeout(function(){
    				console.log("Show Tool Tip");
    				toolTip = baseSvg.append("rect").attr("x", function(){
    					return currentNode.attr("cx");
    				}).attr("y", function(){
    					return currentNode.attr("cy");
    				}).attr("width", 100).attr("height", 40).attr("fill", function(){
    					return getLevelColour(parseInt(currentNode.attr("data-level")));
    				}).attr("stroke", "black")

    				//$(toolTip).css('display', 'none');

    				$(toolTip).fadeIn('slow');
    			}, 1000)
    		},
    		mouseleave : function(){
    			clearTimeout(window.mytimeout);
    			toolTip.remove();
    			
    			console.log("exit");
    		}
    	});

    	//Qualification Sections
    	console.log("No. Qual Sections: " + newCircles.length);
    	$.each(newCircles, function(index, value){
    		var el = $("<div class='col-md-5 col-sm-5 qualifification-section'></div>");
			$("#qualification-container").append(el);
			el.append("<div class='edit-button' role='button'> <a href='./pathway/edit-qualification/" + value.qualification + "''>Edit [X]</a></div>");
			el.append("<div>" + value.qualification + "</div>");

			var li = $("<ul></ul>");
			el.append(li);

			$.each(value.subjects[0], function(index2, value2){
				li.append("<li>" + value2.__data__.name + "</li>");
				console.log(value2.__data__.name);
			});
    	});

	});
	
	


});

function getLevelColour(i) {
	switch(i) {
		case 1:
			return "orange"
		case 2:
			return "red"
		case 3:
			return "yellow"
		case 4:
			return "cyan"
		case 5:
			return "coral"
		case 6:
			return "blue"
		default:
			return "green"
	}
}

function getLevelClass(i) {
	switch(i) {
		case 1:
			return "node node-level-1"
		case 2:
			return "node node-level-2"
		case 3:
			return "node node-level-3"
		case 4:
			return "node node-level-4"
		case 5:
			return "node node-level-5"
		case 6:
			return "node node-level-6"
		default:
			return "node"
	}
}