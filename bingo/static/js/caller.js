var callerSocket;
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

  callerSocket = new WebSocket(ws_scheme + window.location.host + "/ws/call/");
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
    if (e.code != 1000) {
      if (!navigator.onLine) {
        alert("You are offline. Please connect to the Internet and try again.");
      } else {
        callerSocket = new WebSocket(
          ws_scheme + window.location.host + "/ws/call/"
        );
      }
    }
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
        exists = false;
        $("#activity > div").each(function (index, element) {
          if (element.id == data.card_id) {
            exists = true;
          }
        });
        if (!exists) {
          $("#activity").append(
            '<div id="' +
              data.card_id +
              '" class="alert alert-success alert-dismissible text-center" role="alert"><button data-dismiss="alert" id="accept" onclick="accept(\'' +
              data.card_id +
              "','" +
              data.name +
              "','" +
              data.team +
              '\')" type="button" class="close mr-5"><span aria-hidden="true">&check;</span></button><button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span></button><span id="message">' +
              data.bingo_alert +
              "</span></div>"
          );
          alert("Someone called bingo!");
        }
        break;
    }
  };
  bingoSocket.onclose = function (e) {
    if (e.code != 1000) {
      if (!navigator.onLine) {
        alert("You are offline. Please connect to the Internet and try again.");
      } else {
        bingoSocket = new WebSocket(
          ws_scheme + window.location.host + "/ws/bingo/"
        );
      }
    }
  };
});
function accept(id, name, team) {
  callerSocket.send(
    JSON.stringify({
      type: "accept",
      id: id,
      name: name,
      team: team,
    })
  );
}
