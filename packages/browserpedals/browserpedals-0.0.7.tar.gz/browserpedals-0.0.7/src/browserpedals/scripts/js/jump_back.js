var latestTime = arguments[0];
var JUMP_BACK_SEC = arguments[1];

function jumpBack(vid) {
    var jumpTime = 0;
    if (vid && (vid.currentTime > JUMP_BACK_SEC)) {
        jumpTime = vid.currentTime;
        vid.currentTime -= JUMP_BACK_SEC;
    }
    return jumpTime;
}

var timestamp = "0";
if (document.documentElement && document.documentElement.hasAttribute("data-last-manually-played-element-timestamp")) {
    timestamp = document.documentElement.getAttribute("data-last-manually-played-element-timestamp");
}

var frameLatestTime = Number(timestamp);
if (frameLatestTime > latestTime) {
    latestTime = frameLatestTime;
}
timestamp = latestTime.toString();

var jumpTimestamp = "0";

if (timestamp != "0") {
    elem = document.querySelector('[data-manually-played-element-timestamp="' + timestamp + '"]')
    if (elem) {
        var jumpTime = jumpBack(elem);
        jumpTimestamp = jumpTime.toString();
    } else {
        timestamp = "0";
    }
}

const obj = {};
obj["timestamp"] = timestamp;
obj["jump_timestamp"] = jumpTimestamp;

var resStr = JSON.stringify(obj);
return resStr;

