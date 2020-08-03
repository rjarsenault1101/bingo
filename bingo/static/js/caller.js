$(document).ready(function () {
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

  document.querySelector("#callnumber").onclick = function (e) {
    callerSocket.send(
      JSON.stringify({
        type: "call",
      })
    );
  };
  document.querySelector("#resetnumbers").onclick = function (e) {
    callerSocket.send(
      JSON.stringify({
        type: "reset",
      })
    );
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
        $("#message").append(
          '<div class="alert alert-success alert-dismissible text-center" role="alert"><button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span></button>Someone called bingo!</div>'
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
      case "logout":
        users = data.users;
        $("#activeusers").text("Active users: " + users);
    }
  };
  bingoSocket.onclose = function (e) {
    console.error("Bingo socket closed unexpectedly");
  };
});
