(function ($) {
  $(".cell").click(function (e) {
    e.preventDefault();
    var color = $(this).css("background-color");
    if (color == "rgb(92, 135, 39)") {
      $(this).addClass("upei-gold");
    } else {
      $(this).removeClass("upei-gold");
    }
    e.stopImmediatePropagation();
  });
})(jQuery);
