$(document).ready(function(){

	var test = [1, 2, 3, 4, 5, 6];
	
	treeJSON = d3.json("../static/js/data.json", function(error, treeData) {
		console.log("data.json loaded");
		console.log(treeData);
		console.log(Object.keys(treeData));

		var viewerWidth = $("#pathway-container").width();
    	var viewerHeight = $("#pathway-container").height();

    	var baseSvg = d3.select("svg")
        baseSvg.attr("width", viewerWidth).attr("height", viewerHeight);

    	var tree = d3.layout.tree().size([viewerHeight, viewerWidth]);

		var j = 0;
		var newCircles = [];

		$.each(treeData, function(index, value){
    		//console.log(value);

    		var circles = baseSvg.selectAll('circle').data(value.subjects);

	        newCircles[j] = {qualification: index ,level: value.level, subjects: circles.enter()};
	        j++;			
    	});

    	console.log(newCircles);

    	$.each(newCircles, function(index, value){
    		console.log(value)

    		value.subjects.append('circle').attr('cx', function(d, i){
				return (i+1) * 40;
			}).attr('cy', function(d, i){
				return (index+1) * 40;
			}).attr('r', '10').attr('data-subject', function(d){
				return d.name;
			}).attr('data-qualification', function(){
				return value.qualification
			}).attr('data-level', function(){
				return value.level;
			})
			.attr('class', function(){
				switch(value.level) {
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
			});
    	});
	});
});