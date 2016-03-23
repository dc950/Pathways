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

    		var circles = baseSvg.selectAll('circle').data(value.subjects).sort(value.level);

	        newCircles[j] = {qualification: index ,level: value.level, subjects: circles.enter()};
	        j++;			
    	});

    	//var noLevels = console.log("Length : " + newCircles.length);
		columnWidth = (viewerWidth - (2 * marginWidth)) / newCircles.length;
		$("#clip1").prepend("<rect x='200' y='10' width=" + columnWidth + " height=" + nav_offset +"/>")

    	/*
    	 * Draw Nodes on screen for every subject undertaken
    	 */
    	$.each(newCircles, function(index, value){
    		//console.log(index)

    		var xPos = (columnWidth * index) + marginWidth;
    		

    		baseSvg.append("rect").attr("x", xPos).attr("y", nav_offset).attr("width", columnWidth).attr("height", titleHeight)
    		.attr("fill", getLevelColour(value.level));

    		baseSvg.append("text").attr("dx", xPos).attr("dy", 20 +  + nav_offset).text(value.qualification);

    		//console.log(value.subjects[0].length);

    		var yHeight;

    		var cn = value.subjects.append("a").attr("xlink:href", function(d) {
    			if(value.level == '9') {
    				return window.location.protocol + "//" + window.location.host + "/career/" + d.name;
    			}
    			else {
    				return "#";
    			}
    		})
    		.append('circle').attr('cx', function(d, i){
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

			$("<rect></rect>").appendTo("#clip1").attr("x", function(d, i){
				return xPos + (columnWidth / 2) + 20;
			}).attr("y", function(d, i){
				var n = value.subjects[0].length;
				var edgeMargin = 60;

				var workingHeight = viewerHeight - titleHeight - (2 * edgeMargin) - nav_offset;

				if (n > 1) {
					var y = (workingHeight / (n-1)) * i + nav_offset;
				} else {
					var y = workingHeight / 2 + nav_offset;
				}
				
				return y + edgeMargin + titleHeight;
			}).attr('width', columnWidth).attr('height', nav_offset);

			value.subjects.append('g').attr('clip-path', 'url(#clip1)').append('text').attr("dx", function(d, i){
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
    			
    		}
    	});

    	//Qualification Sections
    	

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
		case 7:
			return "Lavender"
		case 8:
			return "SandyBrown"
		case 9:
			return "Gainsboro"
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

function compare(a,b) {
	if (a.level > b.level) {
		return 1;
	} else if (a.level < b.level) {
		return -1;
	} else {
		return 0;
	}
}