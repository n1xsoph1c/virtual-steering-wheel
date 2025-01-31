function enableFullscreen() {
    let doc = document.documentElement;

    if (doc.requestFullscreen) {
        doc.requestFullscreen();
    } else if (doc.mozRequestFullScreen) { // Firefox
        doc.mozRequestFullScreen();
    } else if (doc.webkitRequestFullscreen) { // Chrome, Safari, Edge
        doc.webkitRequestFullscreen();
    } else if (doc.msRequestFullscreen) { // IE
        doc.msRequestFullscreen();
    } else {
        console.warn("❌ Fullscreen not supported on this browser.");
    }
}

// 🔹 Works on Chrome, Firefox, but NOT on iOS Safari
function lockOrientation() {
    if (screen.orientation && screen.orientation.lock) {
        screen.orientation.lock("landscape").catch((err) => {
            console.warn("❌ Orientation lock failed:", err);
        });
    }
}

// 🔹 iOS Safari Fix - Request Orientation Lock Manually
function iosOrientationFix() {
    window.addEventListener("orientationchange", () => {
        if (window.orientation === 90 || window.orientation === -90) {
            console.log("✅ Landscape Mode Enabled");
        } else {
            alert("🔄 Please rotate your device to landscape mode!");
        }
    });
}

// 🔹 Enable fullscreen & orientation lock on user click
document.addEventListener("click", () => {
    enableFullscreen();
    lockOrientation();
    iosOrientationFix();
}, { once: true });
