$(document).ready(function () {
  $.ajax({
    url: "http://" + window.location.host + "/cards",
    contentType: "application/json",
    dataType: "json",
    success: function (result) {
      var data = JSON.parse(result);
      for (var i = 0; i < data.cards.length; i++) {
        $("#card-ids").append(
          '<a id="' +
            data.cards[i] +
            '" class="dropdown-item" onclick="return toggleCollapse()">' +
            data.cards[i] +
            "</a>"
        );
      }
    },
  });
});

function toggleCollapse() {
  $("#user-card tbody").empty();
  var id = $(event.target).text();
  $.ajax({
    url: "http://" + window.location.host + "/" + id,
    contentType: "application/json",
    dataType: "json",
    success: function (result) {
      var data = JSON.parse(result);
      // append rows to table body
      for (var i = 0; i < data.numbers.length; i += 5) {
        var row = '<tr class="cardRow">';
        for (var j = i; j < i + 5; j++) {
          row += "<td ";
          if ($.inArray(data.numbers[j], data.called) >= 0) {
            row += 'class="upei-gold"';
          }
          if (data.numbers[j] === "FREE") {
            row += 'class="upei-gold"';
          }
          row += ">" + data.numbers[j] + "</td>";
        }
        row += "</tr>";
        $("#user-card tbody").append(row);
        $("#cardcollapse").collapse("show");
      }
      return false;
    },
  });
}

const callerSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/call/"
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
      prevNum = 0;
  }
};
callerSocket.onclose = function (e) {
  console.error("Chat socket closed unexpectedly");
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
  "ws://" + window.location.host + "/ws/bingo/"
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
          '<a id="' +
            data.card_id +
            '" class="dropdown-item" onclick="return toggleCollapse()">' +
            data.card_id +
            "</a>"
        );
      }
      break;
  }
};
