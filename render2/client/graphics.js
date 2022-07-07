import * as THREE from 'three';

let camera, scene, renderer;
let mesh;

init();
animate();

function init() {

    camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 1, 1000 );
    camera.position.z = 400;

    scene = new THREE.Scene();

    var loader = new THREE.TextureLoader();
    loader.load( './textures/grid512.jpg', function ( texture ) {

        var geometry = new THREE.SphereGeometry( 200, 20, 20 );

        var material = new THREE.MeshBasicMaterial( { map: texture } );
        mesh = new THREE.Mesh( geometry, material );
        scene.add( mesh );

    } );

    renderer = new THREE.WebGLRenderer( { antialias: true } );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.body.appendChild( renderer.domElement );

    window.addEventListener( 'resize', onWindowResize );
}

function onWindowResize() {

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize( window.innerWidth, window.innerHeight );

}

function animate() {

    requestAnimationFrame( animate );

    if(mesh) {
        mesh.rotation.x += 0.005;
        mesh.rotation.y += 0.01;
    }

    renderer.render( scene, camera );

}
