precision mediump float;

varying vec2 vPos;

// Important: This value must be equal to or greater than u_circleCount
// This is required since the shader must use a defined constant and
// cannot use a Uniform value to define the array size
const int MAX_CIRCLES = 400;

// Used to determine the edge range with smoothstep
const float maskFeather = 0.01;

// Set darkness factor of the masked area 0.0 - 1.0, where 0.0 is black
const float maskDarkness = 0.2;

// Uniforms. Must be sent from the JavaScript side
uniform int u_frame;
uniform int u_circleCount;
uniform float u_circleRadius;
uniform vec2 u_circlePositions[MAX_CIRCLES];
uniform vec3 u_circleColors[MAX_CIRCLES];
uniform float u_maskRadius;

void main() {

  // Draw a black background
  gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);

  // Initialize the color to black (0., 0., 0.)
  vec3 colour = vec3(0.0);

  // Loop through maximum array size of u_circlePositions/u_circleColors
  for (int i = 0; i < MAX_CIRCLES; i ++) {

    // Break out if i is greater than the number of circles
    if (i >= u_circleCount) {
      continue;
    }

    // Define the base color for the circle
    vec3 col = u_circleColors[i];

    // Calculate the distance from the current pixel to the circle
    float d = length(vPos - u_circlePositions[i].xy);
    float r = u_circleRadius;

    // Option 1: Solid circles
    // if (d < r) {
    //   colour += col;
    // }

    // Option 2: Linear Gradient circles
    // float gradient = 1.0 - smoothstep(r * 0.2, r, d);
    // colour += col * gradient;

    // Option 3: Inverse Square gradient to more naturally model light
    // 1. Calculate normalized distance
    // 2. Apply inverse square law
    // Add 1.0 to avoid division by zero at the center
    float normalizedDistance = d / r;
    float gradient = 1.0 / (1.0 + normalizedDistance * normalizedDistance);
    colour += col * gradient;
  }

  // Calculate pixel distance from center (0, 0) for masking purposes
  float distFromCenter = distance(vPos, vec2(0.0));

  // Option 1: Hard mask
  // if (distFromCenter > u_maskRadius) {
  //   colour = colour * step(distFromCenter, u_maskRadius);
  // }

  // Option 2: Smooth mask
  float maskValue = smoothstep(u_maskRadius - maskFeather, u_maskRadius, distFromCenter);
  colour = mix(colour, colour * maskDarkness, maskValue);

  gl_FragColor = vec4(colour, 1.);
}