$(document).ready(function() {
	$(".b").click(function(){
		console.log("Inside function")
		$.ajax({
			type: "GET",
			url: "/mod",
			data: {
				"text": "Bye everyone",
			},
			dataType: "html",
		})
		.done(function(response) {
			console.log("Success");
			$("#test").html(response);
		})
		.fail(function() {
			console.log("Error while sending the data");
		}) 
		
	})
})

/*$.get("/mod",{"text": "Vye everyone"},function(data) {
			console.log("Success");
			console.log(data)
			$("#test").html(data);
		})*/