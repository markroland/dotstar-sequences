// Variables that can be adjusted per preference/setup
const canvasWidth = 800;
const canvasHeight = 800;

// LED strip geometry
// Important: the number of LEDs is determined by the width of the image
// ringRadius: The radius of the LED ring
// circleRadius: The radius of the circle representing the LED ring.
//   A value of 1 is the distance from the canvas center to the canvas edge
//   (as defined by vertexPositions)
// maskRadius: The radius of a mask outside of which LED light is blocked
const ringRadius = 0.75;
const circleRadius = 0.03;
const maskRadius = ringRadius;

// This adjusts the intensity of the RGB color values. Range: 0.0 - 1.0
const intensityFactor = 0.3;

// Image source for the LED Sequence
const img_source = 'rainbow.png';

// Optional: Determine the period using the image height and a preferred
// frame rate, i.e. (500 rows * 1000 ms/s) / 20 fps = 25000 ms
const img_period = 5000;

// Set the frame rate in seconds
// Set to null to use requestAnimationFrame instead of setTimeout
const frameRate = 1/30;

// Define the global variables
let imageData, imageWidth, imageHeight;

/**
 * Loads an image from the given source URL and extracts its pixel data.
 * @param {string} src - The URL of the image to load.
 * @async
 */
async function loadImage(src) {
    const img = new Image();
    img.src = src;

    try {
        await img.decode();

        imageWidth = img.width;
        imageHeight = img.height;

        // Create OffscreenCanvas
        const offscreen = new OffscreenCanvas(imageWidth, imageHeight);
        const ctx = offscreen.getContext('2d');

        // Draw image onto the offscreen canvas
        ctx.drawImage(img, 0, 0);

        // Get image data from the offscreen canvas
        imageData = ctx.getImageData(0, 0, imageWidth, imageHeight).data;

    } catch (error) {
        console.error("Error loading image:", error);
    }
}

/**
 * Loads the vertex and fragment shaders from the given URLs.
 * @param {string} vertexShaderSrc - The URL of the vertex shader.
 * @param {string} fragmentShaderSrc - The URL of the fragment shader.
 * @returns {{vertexShaderSource: string, fragmentShaderSource: string} | null} An object containing the shader source code, or null if an error occurred.
 */
async function loadShaders(vertexShaderSrc, fragmentShaderSrc) {
    try {
        const [vertexShaderResponse, fragmentShaderResponse] = await Promise.all([
            fetch(vertexShaderSrc),
            fetch(fragmentShaderSrc)
        ]);

        if (!vertexShaderResponse.ok) {
            throw new Error(`Vertex shader HTTP error ${vertexShaderResponse.status}`);
        }
        if (!fragmentShaderResponse.ok) {
            throw new Error(`Fragment shader HTTP error ${fragmentShaderResponse.status}`);
        }

        const vertexShaderSource = await vertexShaderResponse.text();
        const fragmentShaderSource = await fragmentShaderResponse.text();
        return { vertexShaderSource, fragmentShaderSource };

    } catch (error) {
        console.error("Error loading shaders:", error);
        return null;
    }
}

/**
 * Creates a shader from the given source code.
 * @param {WebGLRenderingContext} gl - The WebGL rendering context.
 * @param {number} type - The type of shader (gl.VERTEX_SHADER or gl.FRAGMENT_SHADER).
 * @param {string} source - The shader source code.
 * @returns {WebGLShader | null} The created shader, or null if compilation failed.
 * @throws {Error} If the shader compilation fails. The error message includes the shader compilation log.
 */
function createShader(gl, type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        const shaderType = type === gl.VERTEX_SHADER ? 'vertex' : 'fragment';
        console.error(`${shaderType} shader compilation error:`, gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
    }
    return shader;
}

/**
 * The main function that initializes the WebGL context, loads the shaders, and renders the animation.
 */
async function main() {

    const canvas = document.getElementById("canvas");
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;

    // Load the control image
    await loadImage(img_source)

    console.log('Imaged Loaded. Width: ' + imageWidth + ', Height: ' + imageHeight);

    // Define the number of LEDSs, and thus circles used to represent their light
    const NUMBER_OF_LEDS = imageWidth;

    const gl = canvas.getContext("webgl");

    if (gl) {
        const version = gl.getParameter(gl.VERSION);
        if (version.startsWith("WebGL 2")) {
            console.log("WebGL 2.0 is supported");
        } else {
            console.log("WebGL 1.0 is supported (version " + gl.VERSION + ")");
        }
    } else {
        console.error("Unable to initialize WebGL. Your browser or machine may not support it.");
        return;
    }

    // Load the shaders
    const shaders = await loadShaders("vertexShader.glsl", "fragmentShader.glsl");
    if (!shaders) {
        console.error("Error loading shaders");
        return;
    }

    const vertexShader = createShader(gl, gl.VERTEX_SHADER, shaders.vertexShaderSource);
    const fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, shaders.fragmentShaderSource);

    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);

    gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.error('Unable to link the shader program: ' + gl.getProgramInfoLog(program));
        return null;
    }

    gl.useProgram(program);

    // Get the location of the uniform variables
    const frameUL = gl.getUniformLocation(program, 'u_frame');
    const circleCountUL = gl.getUniformLocation(program, 'u_circleCount');
    const circleRadiusUL = gl.getUniformLocation(program, 'u_circleRadius');
    const circlePositionsUL = gl.getUniformLocation(program, 'u_circlePositions');
    const circleColorsUL = gl.getUniformLocation(program, 'u_circleColors');
    const maskRadiusUL = gl.getUniformLocation(program, 'u_maskRadius');

    const positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    const vertexPositions = new Float32Array([
        -1.0, -1.0,
        1.0, -1.0,
        -1.0, 1.0,
        1.0, 1.0,
    ]);
    gl.bufferData(gl.ARRAY_BUFFER, vertexPositions, gl.STATIC_DRAW);

    const positionLocation = gl.getAttribLocation(program, "aPosition");
    gl.enableVertexAttribArray(positionLocation);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

    function render() {

        // console.log("Rendering frame: " + frame);

        const circlePositions = [];
        const circleColors = [];

        let theta = 0;
        const imageRow = frame * imageWidth * 4;
        for (let i = 0; i < NUMBER_OF_LEDS; i++) {

            // Position of LED
            theta = (Math.PI * 2) * (i / NUMBER_OF_LEDS);
            const x = Math.cos(theta) * ringRadius;
            const y = Math.sin(theta) * ringRadius;

            circlePositions.push(x, y);

            // Color of LED
            const r = intensityFactor * imageData[imageRow + i * 4] / 255;
            const g = intensityFactor * imageData[imageRow + i * 4 + 1] / 255;
            const b = intensityFactor * imageData[imageRow + i * 4 + 2] / 255;
            circleColors.push(r, g, b);
        }

        // Update the frame uniform
        gl.uniform1i(frameUL, frame);
        gl.uniform1i(circleCountUL, NUMBER_OF_LEDS);
        gl.uniform1f(circleRadiusUL, circleRadius);
        gl.uniform2fv(circlePositionsUL, circlePositions);
        gl.uniform3fv(circleColorsUL, circleColors);
        gl.uniform1f(maskRadiusUL, maskRadius);

        gl.clearColor(0, 0, 0, 1);
        gl.clear(gl.COLOR_BUFFER_BIT);

        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);

        // Loop the frame based on the image height
        frame = (frame + 1) % imageHeight;

        if (frameRate) {
            setTimeout(render, frameRate * 1000);
        } else {
            requestAnimationFrame(render);
        }
    }

    let frame = 0;
    render();
}

// Run the main function
main();