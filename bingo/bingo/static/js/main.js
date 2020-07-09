
(function ($) {
	$("td").click(function(e) {   
		e.preventDefault();
		var color = $(this).css("background-color");
		console.log(color);
		if(color == 'rgb(92, 135, 39)'){
			$(this).css("background-color","#aaaa00");
		} else {
			$(this).css("background-color","#5c8727");
		}
		e.stopImmediatePropagation();
	  });
})(jQuery);