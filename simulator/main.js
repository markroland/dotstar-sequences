import * as THREE from 'three';

import Stats from 'three/addons/libs/stats.module.js';

import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RectAreaLightHelper } from 'three/addons/helpers/RectAreaLightHelper.js';
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';

let renderer, scene, camera;
let stats;
let Lights = [];
let imageData, imageWidth, imageHeight;

// Important: the number of lights is determined by the width of the image

// Variables that can be adjusted per preference/setup
const img_source = 'rainbow.png';
const img_period = 5000; // Optional: Determine the period using the image height and a preferred frame rate, i.e. (500 rows * 1000 ms/s) / 20 fps = 25000 ms
const radius = 50;
const lightIntensity = 10;
const lightYpos = 2;

init();

/**
 * Initialize the ThreeJS scene
 **/
function init() {

    renderer = new THREE.WebGLRenderer( { antialias: true } );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    renderer.setAnimationLoop( animation );
    renderer.outputEncoding = THREE.sRGBEncoding;
    document.body.appendChild( renderer.domElement );

    camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 1000 );
    camera.position.set( 0, 200, 0 );

    scene = new THREE.Scene();

    RectAreaLightUniformsLib.init();

    const geoFloor = new THREE.CircleGeometry( radius, 120 );
    geoFloor.rotateX(-Math.PI / 2);
    const matStdFloor = new THREE.MeshStandardMaterial( { color: 0xFFFFFF, roughness: 0.5, metalness: 0 } );
    const mshStdFloor = new THREE.Mesh( geoFloor, matStdFloor );
    scene.add( mshStdFloor );

    const controls = new OrbitControls( camera, renderer.domElement );
    controls.update();

    window.addEventListener( 'resize', onWindowResize );

    stats = new Stats();
    document.body.appendChild( stats.dom );

    // Load the control image
    loadImage(img_source).then(() => {

        console.log('Imaged Loaded. Width: ' + imageWidth + ', Height: ' + imageHeight);

        // Add lights to the scene
        let theta = 0;
        const NUMBER_OF_LEDS = imageWidth;
        const lightWidth = 0.5 * (2 * radius * Math.sin(Math.PI / NUMBER_OF_LEDS));
        const lightHeight = lightWidth;
        for (let i = 0; i < NUMBER_OF_LEDS; i++) {
            Lights[i] = new THREE.RectAreaLight(0x000000, lightIntensity, lightWidth, lightHeight );
            theta = (i/NUMBER_OF_LEDS) * (2 * Math.PI);
            let x = radius * Math.cos(theta);
            let z = radius * Math.sin(theta);
            Lights[i].position.set( x, lightYpos, z );
            Lights[i].lookAt( 0, lightYpos, 0 );
            scene.add( Lights[i] );
            scene.add( new RectAreaLightHelper( Lights[i] ) );
        }
    })
}

/**
 * Load an image that defines the light sequence animation
 **/
async function loadImage(img_src) {
    const img = new Image();
    img.src = img_src;
    // For images from a different origin (domain, protocol, or port)
    // img.crossOrigin = "";  // or img.crossOrigin = "anonymous";

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
 * Window resize event handler
 **/
function onWindowResize() {
    renderer.setSize( window.innerWidth, window.innerHeight );
    camera.aspect = ( window.innerWidth / window.innerHeight );
    camera.updateProjectionMatrix();
}

/**
 * Animation loop for renderer
 **/
function animation( time ) {
    setLightsFromImage(time, img_period);
    renderer.render( scene, camera );
    stats.update();
}

/**
 * Set the color of the ThreeJS lights based on the image data.
 * @param {number} time -Elapsed time in milliseconds since the start of the animation
 * @param {number} period The duration of the sequence in the image. Each frame will get the period / image-height
 **/
function setLightsFromImage(time, period) {

    const row = Math.floor((time % period) / period * imageHeight);

    for (let x = 0; x < imageWidth; x++) {
        const index = (row * imageWidth + x) * 4;

        const r = imageData[index];
        const g = imageData[index + 1];
        const b = imageData[index + 2];

        // Now you have the RGB values for the pixel at (x, y).
        // Use these values to set the lights. Example:
        const pixelColor = new THREE.Color(r / 255, g / 255, b / 255);

        if (Lights[x]) {
            Lights[x].color.set(pixelColor);
        }
    }
}