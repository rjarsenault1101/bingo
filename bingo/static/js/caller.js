$(document).ready(function () {
  if (window.location.protocol == "https:") {
    var http_scheme = "https://";
    var ws_scheme = "wss://";
  } else {
    var http_scheme = "http://";
    var ws_scheme = "ws://";
  }

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

  const callerSocket = new WebSocket(
    ws_scheme + window.location.host + "/ws/call/"
  );
  prevNum = 0;
  callerSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    switch (data.type) {
      case "call_number":
        console.log(data.number);
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
        $("#activity").append(data.bingo_alert + "\n");
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
    console.error(e);
  };
});
