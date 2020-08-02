$(document).ready(function () {
  /*
   * LAUNCH STUFF
   */
  if (window.location.protocol == "https:") {
    var http_scheme = "https://";
    var ws_scheme = "wss://";
  } else {
    var http_scheme = "http://";
    var ws_scheme = "ws://";
  }
  rows = $.each($("#numbergrid tbody tr"), function (
    indexInArray,
    valueOfElement
  ) {
    bingo = ["B", "I", "N", "G", "O"];
    $.each($(valueOfElement).find("td"), function (
      indexInArray2,
      valueOfElement2
    ) {
      valueOfElement2.prepend(bingo[indexInArray]);
    });

    $(
      '<td style="background-color: #333333;">' + bingo[indexInArray] + "</td>"
    ).prependTo($(valueOfElement));
  });
  $.ajax({
    url: http_scheme + window.location.host + "/cards",
    contentType: "application/json",
    dataType: "json",
    success: function (result) {
      var data = JSON.parse(result);
      for (var i = 0; i < data.cards.length; i++) {
        $("#card-ids").append(
          '<button id="' +
            data.cards[i] +
            '" class="dropdown-item" onclick="toggleCollapse();">' +
            data.cards[i] +
            "</button>"
        );
      }
    },
  });

  /*
   * BUTTON HANDLERS
   */
  $("#callnumber").click(function () {
    callerSocket.send(
      JSON.stringify({
        type: "call",
      })
    );
  });

  $("#resetnumbers").click(function () {
    callerSocket.send(
      JSON.stringify({
        type: "reset",
      })
    );
  });
  $("#submitnewnumbers").click(function () {
    var newnumbers = $("#newnumbersarea").val();
    newnumbers = newnumbers.split(",");
    newnumbers = newnumbers.map((element) => element.trim());
    cleaned = newnumbers.filter(function (num) {
      return num !== "";
    });
    callerSocket.send(
      JSON.stringify({
        type: "resetwithnew",
        values: cleaned,
      })
    );
  });
  /*
   *  WEBSOCKETS
   */

  const callerSocket = new WebSocket(
    ws_scheme + window.location.host + "/ws/call/"
  );
  prevNum = 0;
  callerSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    switch (data.type) {
      case "call_number":
        $("#" + prevNum).removeClass("blink_me");
        $("#" + prevNum).addClass("upei-gold");
        $("#" + data.number).addClass("blink_me");
        prevNum = data.number;
        break;
      case "resetwithnew":
        const values = data.values;
        const body = $("#numbergrid tbody");
        body.empty();
        const cols = values.length / 5;
        for (var j = 0; j < 5; j++) {
          row = $("<tr class='cardRow'></tr>");
          for (var i = 0; i < cols; i++) {
            row.append("<td>" + values[cols * j + i] + "</td>");
          }
          body.append(row);
        }

      // Reset table with new values
      // Divide the data into 5
      case "reset":
        $("td").removeClass("blink_me");
        $("td").removeClass("upei-gold");
        $("#activity").empty();
        prevNum = 0;
    }
  };
  callerSocket.onclose = function (e) {
    console.error("Caller socket closed unexpectedly");
    console.error(e);
  };

  const bingoSocket = new WebSocket(
    ws_scheme + window.location.host + "/ws/bingo/"
  );
  bingoSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    switch (data.type) {
      case "bingo":
        $("#activity").append(
          '<div class="alert alert-success alert-dismissible text-center" role="alert"><button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span></button>' +
            data.bingo_alert +
            "</div>"
        );
        break;
      case "login":
        if (!$("#" + data.card_id).length) {
          $("#card-ids").append(
            '<button id="' +
              data.card_id +
              '" class="dropdown-item" onclick="toggleCollapse();">' +
              data.card_id +
              "</button>"
          );
        }
        break;
    }
  };
  bingoSocket.onclose = function (e) {
    console.error("Bingo socket closed unexpectedly");
  };
});
