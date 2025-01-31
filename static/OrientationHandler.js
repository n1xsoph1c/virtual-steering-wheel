

// async function requestMotionPermission() {
//   if (typeof DeviceMotionEvent.requestPermission === "function") {
//       try {
//           const permissionState = await DeviceMotionEvent.requestPermission();
//           if (permissionState === "granted") {
//               console.log("✅ Motion access granted!");
//           } else {
//               alert("❌ Motion access denied! Please allow motion access in settings.");
//           }
//       } catch (error) {
//           console.error("Error requesting motion permission:", error);
//           alert("❌ Failed to request motion access.");
//       }
//   } else {
//       console.log("✅ No need to request motion permission.");
//   }
// }

// // Call the function on a user interaction
// document.addEventListener("click", requestMotionPermission, { once: true });

// var degtorad = Math.PI / 180; // Degree-to-Radian conversion
// var radtodeg = 180 / Math.PI

// function steeringHeading( alpha, beta, gamma ) {

//     var _x = beta ? beta * degtorad : 0;
//     var _y = gamma ? gamma * degtorad : 0;
//     var _z = alpha ? alpha * degtorad : 0;

//     var cosB = Math.cos(_x)
//     var cosA = Math.cos(_z)
//     var cosG = Math.cos(_y)
//     var sinG = Math.sin(_y)
//     var sinB = Math.sin(_x)
//     var sinA = Math.sin(_z)

//     var Vx = cosB * sinA
//     var Vy = -cosA * cosB

    

    

//     var theta = -Math.atan( Vx / Vy) * radtodeg



//   return theta // Compass Heading (in degrees)

// }


// window.addEventListener(
//   "deviceorientation",
//   function (event) {
//     if (event.alpha === null) {
//       console.warn("⚠️ Gyroscope not available or permission not granted.");
//       return;
//     }

//     let z = event.alpha ? Math.ceil(event.alpha) : 0;
//     let x = event.beta ? Math.ceil(event.beta) : 0;
//     let y = event.gamma ? Math.ceil(event.gamma) : 0;

//     if (y >= 89) y = 89;
//     if (y <= -89) y = -89;

//     let accel = Math.max(0, Math.min(75, 90 + y));
//     let heading = steeringHeading(x, y, z);

//     socket.emit("gyro", { steering: Math.ceil(heading), thrust: accel });
//     document.getElementById("view3d").style.transform = `rotate(${heading}deg)`;

//     console.log(`Gyro: ${heading}° | Accel: ${accel}`);
//   },
//   true
// );


async function requestMotionPermission() {
  if (typeof DeviceMotionEvent.requestPermission === "function") {
      try {
          const permissionState = await DeviceMotionEvent.requestPermission();
          if (permissionState === "granted") {
              console.log("✅ Motion access granted!");
          } else {
              alert("❌ Motion access denied! Please enable motion access in settings.");
          }
      } catch (error) {
          console.error("Error requesting motion permission:", error);
          alert("❌ Failed to request motion access.");
      }
  } else {
      console.log("✅ No need to request motion permission.");
  }
}

// 🔹 Call motion permission function on user interaction
document.addEventListener("click", requestMotionPermission, { once: true });

// 🔹 Gyro Optimization: Only send data if the change > threshold
let lastSteering = 0;
let gyroThreshold = 1.5; // Min change required to send data

function steeringHeading(alpha, beta, gamma) {
  var degtorad = Math.PI / 180;
  var radtodeg = 180 / Math.PI;

  var _x = beta ? beta * degtorad : 0;
  var _y = gamma ? gamma * degtorad : 0;
  var _z = alpha ? alpha * degtorad : 0;

  var cosB = Math.cos(_x);
  var sinA = Math.sin(_z);

  var Vx = cosB * sinA;
  var Vy = -Math.cos(_z) * cosB;

  return -Math.atan(Vx / Vy) * radtodeg;
}

window.addEventListener("deviceorientation", function (event) {
  if (event.alpha === null) {
      console.warn("⚠️ Gyroscope not available or permission not granted.");
      return;
  }

  let z = event.alpha ? Math.ceil(event.alpha) : 0;
  let x = event.beta ? Math.ceil(event.beta) : 0;
  let y = event.gamma ? Math.ceil(event.gamma) : 0;

  if (y >= 89) y = 89;
  if (y <= -89) y = -89;

  let accel = Math.max(0, Math.min(75, 90 + y));
  let heading = steeringHeading(x, y, z);

  // 🔹 Send data only if the change is greater than threshold
  if (Math.abs(heading - lastSteering) > gyroThreshold) {
      socket.emit("gyro", { steering: Math.ceil(heading), thrust: accel });
      lastSteering = heading;
      document.getElementById("view3d").style.transform = `rotate(${heading}deg)`;
      console.log(`📡 Gyro Sent: ${heading}° | Accel: ${accel}`);
  }
}, true);
