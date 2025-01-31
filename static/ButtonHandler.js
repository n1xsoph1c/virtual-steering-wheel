const buttonCooldown = 300; // 300ms cooldown
const longPressDuration = 500; // 500ms to detect long press

let activeInterval = {}; // Store active intervals for each button

document.querySelectorAll("button").forEach((button) => {
    let lastPressed = 0;
    
    button.addEventListener("click", () => {
        let now = Date.now();
        if (now - lastPressed < buttonCooldown) return; // Prevent spam

        lastPressed = now;
        button.classList.add("active");

        // 🔹 Use WebSocket for fast response
        socket.emit("buttonPress", { button: button.id });

        console.log(`🟢 ${button.id} was pressed`);

        setTimeout(() => button.classList.remove("active"), 200);
    });

    button.addEventListener("touchstart", () => {
        button.classList.add("active");
        console.log(`🔵 Long Press Start: ${button.id}`);

        // 🔹 Start emitting button hold events every 100ms
        activeInterval[button.id] = setInterval(() => {
            socket.emit("buttonTouchStart", { button: button.id });
            console.log(`🔄 Holding: ${button.id}`);
        }, 100);
    });

    button.addEventListener("touchend", () => {
        button.classList.remove("active");
        console.log(`🟠 Released: ${button.id}`);

        // 🔹 Stop emitting signals
        clearInterval(activeInterval[button.id]);
        delete activeInterval[button.id];

        socket.emit("buttonTouchEnd", { button: button.id });
    });
});
