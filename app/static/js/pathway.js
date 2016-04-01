$(document).ready(function(){

	var nav_offset = 0;

	var test = [1, 2, 3, 4, 5, 6];

	treeJSON = d3.json("?request_json=1", function(error, treeData) {
		console.log("Loading error: " + error);
		console.log(treeData);

		var viewerWidth = $("#pathway-container").width();
    	var viewerHeight = $("#pathway-container").height();

    	var marginWidth = 10;
    	var columnWidth;

    	var titleHeight = 30;

    	var baseSvg = d3.select("#pathway-svg")
        baseSvg.attr("width", viewerWidth).attr("height", viewerHeight);

    	var tree = d3.layout.tree().size([viewerHeight, viewerWidth]);

		var j = 0;
		var newCircles = [];


		$.each(treeData, function(index, value){
    		var circles = baseSvg.selectAll('circle').data(value.subjects).sort(value.level);
			newCircles[j] = {qualification: index , short_name: value.short_name, level: value.level, subjects: circles.enter()};
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
    		console.log(value);
    		baseSvg.append("text").attr("dx", xPos).attr("dy", 20 +  + nav_offset).text(value.short_name);


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

			}).attr('r', '10').attr('data-subject', function(d){
				return d.name;
			}).attr('data-qualification', function(){
				return value.qualification
			}).attr('data-future', function(d){
				console.log(d.future);
				return d.future;
			}).attr('data-level', function(){
				return value.level;
			}).attr('class', function(d){
				if (d.future) {
					 return "node node-future";
				} else {
					return "node";
				}
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

			value.subjects.append('text').attr("dx", function(d, i){
				return xPos;
			}).attr("dy", function(d, i){
				var n = value.subjects[0].length;
				var edgeMargin = 60;

				var workingHeight = viewerHeight - titleHeight - (2 * edgeMargin) - nav_offset;

				if (n > 1) {
					var y = (workingHeight / (n-1)) * i + nav_offset;
				} else {
					var y = workingHeight / 2 + nav_offset;
				}
				
				return y + edgeMargin + titleHeight + 25;
			}).text(function(d){
				return d.name;
			}).attr('class', 'node-label hidden-xs');

    	});
	});
	
	


});

function getLevelColour(i) {
	switch(i) {
		case 2:
			return "#96ceb4"
		case 3:
			return "#ffeead"
		case 4:
			return "#ff6f69"
		case 5:
			return "#ffcc5c"
		case 6:
			return "#b3cde0"
		case 7:
			return "#be9b7b"
		case 8:
			return "#fffeb3"
		case 9:
			return "#f1cbff"
		default:
			return "white"
	}
}

function getLevelClass(i) {
	if (true) {
		return "node node-future";
	} else {
		return "node";
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