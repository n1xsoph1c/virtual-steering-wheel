var degtorad = Math.PI / 180; // Degree-to-Radian conversion
var radtodeg = 180 / Math.PI

function steeringHeading( alpha, beta, gamma ) {

    var _x = beta ? beta * degtorad : 0;
    var _y = gamma ? gamma * degtorad : 0;
    var _z = alpha ? alpha * degtorad : 0;

    var cosB = Math.cos(_x)
    var cosA = Math.cos(_z)
    var cosG = Math.cos(_y)
    var sinG = Math.sin(_y)
    var sinB = Math.sin(_x)
    var sinA = Math.sin(_z)

    var Vx = cosB * sinA
    var Vy = -cosA * cosB

    

    

    var theta = -Math.atan( Vx / Vy) * radtodeg



  return theta // Compass Heading (in degrees)

}