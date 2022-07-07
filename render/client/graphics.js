import * as THREE from 'three';

import { OrbitControls } from './jsm/controls/OrbitControls.js';

let cameraPersp, cameraOrtho, currentCamera;
let scene, renderer, orbit;
let sphere;

init();
render();

function init() {

    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.body.appendChild( renderer.domElement );

    const aspect = window.innerWidth / window.innerHeight;

    // add camera
    cameraPersp = new THREE.PerspectiveCamera( 50, aspect, 0.01, 30000 );
    cameraOrtho = new THREE.OrthographicCamera( - 600 * aspect, 600 * aspect, 600, - 600, 0.01, 30000 );
    currentCamera = cameraPersp;

    currentCamera.position.set( 500, 250, 500 );
    currentCamera.lookAt( 0, 200, 0 );

    scene = new THREE.Scene();

    // add textured sphere
    const texture_world = new THREE.TextureLoader().load( 'textures/grid512.jpg', render );
    texture_world.anisotropy = renderer.capabilities.getMaxAnisotropy();

    sphere = new THREE.SphereGeometry( 200, 200, 200 );
    const globe_material = new THREE.MeshLambertMaterial( { map: texture_world, transparent: true } );
    const globe_mesh = new THREE.Mesh( sphere, globe_material )
    scene.add( globe_mesh );

    // add user location indicator
    const texture_cursor = new THREE.TextureLoader().load( 'textures/cursor.png', render );
    texture_cursor.anisotropy = renderer.capabilities.getMaxAnisotropy();

    const cursor = new THREE.SphereGeometry( 5, 5, 5 );
    const cursor_material = new THREE.MeshLambertMaterial( { map: texture_cursor, transparent: true } );
    const cursor_mesh = new THREE.Mesh( cursor, cursor_material )
    scene.add( cursor_mesh );
    cursor_mesh.position.set(200,0,0);

    // add lighting

    // todo; add sun that rotates corresponding to in game time
    // const light = new THREE.DirectionalLight( 0xf0f0f0, 2 );
    // light.position.set( 1, 1, 1 );
    // scene.add( light );

    const ambientLight = new THREE.AmbientLight( 0xffffff ); // soft white light
    scene.add( ambientLight );

    // add mouse interactions
    orbit = new OrbitControls( currentCamera, renderer.domElement );
    orbit.update();
    orbit.addEventListener( 'change', render );

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
