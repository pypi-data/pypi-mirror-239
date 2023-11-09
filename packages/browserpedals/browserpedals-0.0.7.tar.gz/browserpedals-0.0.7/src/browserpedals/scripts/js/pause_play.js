var latestTime = arguments[0];

function pausePlay(vid) {
    var pauseTime = 0;
    var playTime = 0;
    if (vid) {
        if (vid.paused || vid.ended) {
            playTime = vid.currentTime;
            vid.play();
        } else {
            vid.pause();
            pauseTime = vid.currentTime;
        }
    }
    return [pauseTime, playTime];
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

var pauseTimestamp = "0";
var playTimestamp = "0";

if (timestamp != "0") {
    elem = document.querySelector('[data-manually-played-element-timestamp="' + timestamp + '"]')
    if (elem) {
        var res = pausePlay(elem);
        var pauseTime = res[0];
        var playTime = res[1];
        pauseTimestamp = pauseTime.toString();
        playTimestamp = playTime.toString();
    } else {
        timestamp = "0";
    }
}

const obj = {};
obj["timestamp"] = timestamp;
obj["pause_timestamp"] = pauseTimestamp;
obj["play_timestamp"] = playTimestamp;

var resStr = JSON.stringify(obj);
return resStr;

