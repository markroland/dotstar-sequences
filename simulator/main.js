
import * as THREE from 'three';

import Stats from 'three/addons/libs/stats.module.js';

import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RectAreaLightHelper } from 'three/addons/helpers/RectAreaLightHelper.js';
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';

let renderer, scene, camera;
let stats;
let Lights = [];

init();

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

    const radius = 50;
    const floor_side = 2 * radius;
    let theta = 0;
    const i_max = 201;
    const lightIntensity = 50;
    // const lightWidth = 5;
    const lightWidth = 0.5 * (2 * radius * Math.sin(Math.PI / i_max));
    const lightHeight = lightWidth;
    let y = 2;
    for (let i = 0; i < i_max; i++) {
        Lights[i] = new THREE.RectAreaLight(0x000000, lightIntensity, lightWidth, lightHeight );
        theta = (i/i_max) * (2 * Math.PI);
        let x = radius * Math.cos(theta);
        let z = radius * Math.sin(theta);
        Lights[i].position.set( x, y, z );
        Lights[i].lookAt( 0, y, 0 );
        scene.add( Lights[i] );
        scene.add( new RectAreaLightHelper( Lights[i] ) );
    }

    const geoFloor = new THREE.BoxGeometry( floor_side, 0.1, floor_side );
    const matStdFloor = new THREE.MeshStandardMaterial( { color: 0xFFFFFF, roughness: 0.5, metalness: 0 } );
    const mshStdFloor = new THREE.Mesh( geoFloor, matStdFloor );
    scene.add( mshStdFloor );

    const controls = new OrbitControls( camera, renderer.domElement );
    controls.update();

    window.addEventListener( 'resize', onWindowResize );

    stats = new Stats();
    document.body.appendChild( stats.dom );
}

function onWindowResize() {
    renderer.setSize( window.innerWidth, window.innerHeight );
    camera.aspect = ( window.innerWidth / window.innerHeight );
    camera.updateProjectionMatrix();
}

function animation( time ) {

    // Set pixel colors

    // RGB chase
    /*
    const red = new THREE.Color(0.5, 0, 0);
    const green = new THREE.Color(0, 0.5, 0);
    const blue = new THREE.Color(0, 0, 0.5);
    const num_colors = 3;
    let offset = Math.floor(time / 500) % num_colors;
    for (let i = 0; i < Lights.length; i++) {
        let pixel = red;
        if ((i + offset) % num_colors == 1) {
            pixel = green;
        }
        else if ((i + offset) % num_colors == 2) {
            pixel = blue;
        }
        Lights[i].color.set(pixel);
    }
    //*/

    // Breathe
    breathe(time);

    renderer.render( scene, camera );

    stats.update();
}

function breathe(time) {

    // Breath period in seconds
    const period = 4 * 1000;

    const min_brightness = 0.1;
    const max_brightness = 0.5;

    // normal_brightness = 0.5 + (0.5 * math.sin( self.time * (1/self.period) * 2 * math.pi))
    let normal_brightness = 0.5 + (0.5 * Math.sin(time * (1/period) * 2 * Math.PI));

    // scaled_brightness = self.max_brightness * (normal_brightness * (self.max_brightness - self.min_brightness) + self.min_brightness)
    let scaled_brightness = max_brightness * (normal_brightness * (max_brightness - min_brightness) + min_brightness);

    // Option 1
    const pixel = new THREE.Color().setHSL(0, 0, scaled_brightness);

    // Option 2
    // # Convert to RGB pixels
    // let rgb = HSVtoRGB(0, 0, scaled_brightness);

    // const pixel = new THREE.Color(rgb.r/255, rgb.g/255, rgb.b/255);

    for (let i = 0; i < Lights.length; i++) {
        Lights[i].color.set(pixel);
    }
}

// https://stackoverflow.com/a/17243070
/* accepts parameters
 * h  Object = {h:x, s:y, v:z}
 * OR
 * h, s, v
*/
function HSVtoRGB(h, s, v) {
    var r, g, b, i, f, p, q, t;
    if (arguments.length === 1) {
        s = h.s, v = h.v, h = h.h;
    }
    i = Math.floor(h * 6);
    f = h * 6 - i;
    p = v * (1 - s);
    q = v * (1 - f * s);
    t = v * (1 - (1 - f) * s);
    switch (i % 6) {
        case 0: r = v, g = t, b = p; break;
        case 1: r = q, g = v, b = p; break;
        case 2: r = p, g = v, b = t; break;
        case 3: r = p, g = q, b = v; break;
        case 4: r = t, g = p, b = v; break;
        case 5: r = v, g = p, b = q; break;
    }
    return {
        r: Math.round(r * 255),
        g: Math.round(g * 255),
        b: Math.round(b * 255)
    };
}
