import * as THREE from 'three';

import { OrbitControls } from './jsm/controls/OrbitControls.js';

let cameraPersp, cameraOrtho, currentCamera;
let scene, renderer, control, orbit;

init();
render();

function init() {

    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.body.appendChild( renderer.domElement );

    const aspect = window.innerWidth / window.innerHeight;

    cameraPersp = new THREE.PerspectiveCamera( 50, aspect, 0.01, 30000 );
    cameraOrtho = new THREE.OrthographicCamera( - 600 * aspect, 600 * aspect, 600, - 600, 0.01, 30000 );
    currentCamera = cameraPersp;

    currentCamera.position.set( 500, 250, 500 );
    currentCamera.lookAt( 0, 200, 0 );

    scene = new THREE.Scene();

    const light = new THREE.DirectionalLight( 0xf0f0f0, 2 );
    light.position.set( 1, 1, 1 );
    scene.add( light );

    const ambientLight = new THREE.AmbientLight( 0x808080 ); // soft white light
    scene.add( ambientLight );

    const texture = new THREE.TextureLoader().load( 'textures/grid512.jpg', render );
    texture.anisotropy = renderer.capabilities.getMaxAnisotropy();

    const geometry = new THREE.SphereGeometry( 200, 200, 200 );
    const material = new THREE.MeshLambertMaterial( { map: texture, transparent: true } );

    orbit = new OrbitControls( currentCamera, renderer.domElement );
    orbit.update();
    orbit.addEventListener( 'change', render );

    // control = new TransformControls( currentCamera, renderer.domElement );
    // control.addEventListener( 'change', render );

    // control.addEventListener( 'dragging-changed', function ( event ) {

    //     orbit.enabled = ! event.value;

    // } );

    const mesh = new THREE.Mesh( geometry, material );
    scene.add( mesh );

    control.attach( mesh );
    scene.add( control );

    window.addEventListener( 'resize', onWindowResize );
}

function onWindowResize() {

    const aspect = window.innerWidth / window.innerHeight;

    cameraPersp.aspect = aspect;
    cameraPersp.updateProjectionMatrix();

    cameraOrtho.left = cameraOrtho.bottom * aspect;
    cameraOrtho.right = cameraOrtho.top * aspect;
    cameraOrtho.updateProjectionMatrix();

    renderer.setSize( window.innerWidth, window.innerHeight );

    render();

}

function render() {

    renderer.render( scene, currentCamera );

}
