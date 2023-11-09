if (!document.documentElement)
    return;

if (!document.body)
    return;

var PAUSE_PERIOD_SEC = arguments[0];
var PAUSE_ZONE_SEC = arguments[1];
var PAUSE_PRECISION_SEC = arguments[2];

document.documentElement.setAttribute("data-last-manually-played-element-timestamp", "0");

document.documentElement.setAttribute("data-tab-recent-visibility-timestamps", "");

const VISIBILITY_POLL_PERIOD_MILLISEC = 1500;
const MAX_TIMESTAMPS_COUNT = 5;


// Periodically pause at given time points in the video/audio.
var periodicPauseFunction = function () {
    var quo = Math.floor(this.currentTime / PAUSE_PERIOD_SEC);
    var rem = this.currentTime % PAUSE_PERIOD_SEC;
    if ((quo > 0) && ((rem <= PAUSE_ZONE_SEC) || (rem >= PAUSE_PERIOD_SEC - PAUSE_ZONE_SEC))) {
        this.pause();

        // Shift currentTime forward out of the pause zone 
        // so the video/audio can play again till the next pause.
        if (rem <= PAUSE_ZONE_SEC) {
            this.currentTime = (quo * PAUSE_PERIOD_SEC) + PAUSE_ZONE_SEC + PAUSE_PRECISION_SEC;
        } else {
            this.currentTime = ((quo + 1) * PAUSE_PERIOD_SEC) + PAUSE_ZONE_SEC + PAUSE_PRECISION_SEC;
        }
    }
};

// User starts controlling a video/audio by clicking "Play":
document.addEventListener('play', function(e) {
    e = e || window.event;
    var elem = e.target || e.srcElement;

    var timestamp = Date.now().toString();
    elem.setAttribute("data-manually-played-element-timestamp", timestamp);

    if (PAUSE_PERIOD_SEC > 0) {
        elem.addEventListener("timeupdate", periodicPauseFunction);
    }

    document.documentElement.setAttribute("data-last-manually-played-element-timestamp", timestamp);
}, true);

// User stops controlling a video/audio by clicking anywhere on the video/audio iframe:
document.addEventListener('click', function(e) {
    e = e || window.event;
    var elem = e.target || e.srcElement;

    elem.removeAttribute("data-manually-played-element-timestamp");

    if (PAUSE_PERIOD_SEC > 0) {
        elem.removeEventListener("timeupdate", periodicPauseFunction);
    }

    document.documentElement.setAttribute("data-last-manually-played-element-timestamp", "0");
}, false);

// audio/video has reached the end:
document.addEventListener('ended', function(e) {
    e = e || window.event;
    var elem = e.target || e.srcElement;

    elem.removeAttribute("data-manually-played-element-timestamp");

    if (PAUSE_PERIOD_SEC > 0) {
        elem.removeEventListener("timeupdate", periodicPauseFunction);
    }

    document.documentElement.setAttribute("data-last-manually-played-element-timestamp", "0");
}, true);


// Record the recent times when user selected this tab:

const recentVisibilityTimestamps = [];
var lastTimestampIndex = -1;

function recordTabVisibility() {
    var testTime = Date.now();
    var tabVisibility = document.visibilityState;

    lastTimestampIndex++;
    if (lastTimestampIndex >= MAX_TIMESTAMPS_COUNT) {
        lastTimestampIndex = 0;
    }

    const timestamp = {};
    timestamp["test_time"] = testTime;
    timestamp["tab_visibility"] = tabVisibility;
    recentVisibilityTimestamps[lastTimestampIndex] = timestamp;

    const obj = {};
    obj["recent_visibility_timestamps"] = recentVisibilityTimestamps;
    obj["last_timestamp_index"] = lastTimestampIndex;
    var dataStr = JSON.stringify(obj);

    document.documentElement.setAttribute("data-tab-recent-visibility-timestamps", dataStr);
}

setInterval(recordTabVisibility, VISIBILITY_POLL_PERIOD_MILLISEC);


// Control out-of-DOM audios:

Audio.prototype.overwrite_play = Audio.prototype.play;

const MAX_CONNECTED_PLAY_COUNT = 10;
var connectedPlayCount = 0;

Audio.prototype.play = function() {
    if (!this.isConnected) {
        document.body.appendChild(this);

        Audio.prototype.play = Audio.prototype.overwrite_play;
    } else {
        connectedPlayCount++;
        if (connectedPlayCount > MAX_CONNECTED_PLAY_COUNT) {
            Audio.prototype.play = Audio.prototype.overwrite_play;
            this.play = Audio.prototype.overwrite_play;
        }
    }

    return this.overwrite_play(arguments);
}

