// 🔹 Initialize WebSocket connection
var socket = io(window.location.origin, {
    reconnection: true,
    reconnectionAttempts: 5,
    reconnectionDelay: 2000, // Try reconnecting every 2 seconds
});

socket.on("connect", function () {
    console.log("✅ Connected to server!");
});

socket.on("disconnect", function () {
    console.warn("⚠️ Disconnected! Attempting to reconnect...");
});
