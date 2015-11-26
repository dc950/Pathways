$(document).ready(function(){

	var test = [1, 2, 3, 4, 5, 6];
	
	treeJSON = d3.json("static/js/data.json", function(error, treeData) {
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
    		console.log(index);

    		var circles = baseSvg.selectAll('circle').data(treeData[index].subjects);
	        newCircles[j] = circles.enter();

	        console.log(newCircles[j].size());

			/*newCircles.append('circle').attr('cx', function(d, i){
				return (i+1) * 40;
			}).attr('cy', function(d, i){
				return (j+1) * 40;
			}).attr('r', '10').attr('data-subject', function(d){
				return d.name;
			}).attr('data-qualification', function(d){
				return index
			});*/

			j++;			
    	});

    	$.each(newCircles, function(index, value){
    		value.append('circle').attr('cx', function(d, i){
				return (i+1) * 40;
			}).attr('cy', function(d, i){
				return (index+1) * 40;
			}).attr('r', '10').attr('data-subject', function(d){
				return d.name;
			}).attr('data-qualification', function(d){
				return index
			});
    	});
	});
});