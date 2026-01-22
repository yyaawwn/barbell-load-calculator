from flask import Flask

app = Flask(__name__)

@app.route('/')
def barbell_calculator_3d():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BarLoad 3D - Photorealistic Calculator</title>
        <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
        <!-- Three.js from CDN -->
        <script async src="https://unpkg.com/es-module-shims@1.6.3/dist/es-module-shims.js"></script>
        <script type="importmap">
          {
            "imports": {
              "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
              "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
            }
          }
        </script>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Rajdhani', sans-serif;
                background-color: #1a1a1a; 
                color: #e0e0e0;
                overflow: hidden;
            }
            
            #canvas-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 1;
            }
            
            .ui-container {
                position: relative;
                z-index: 2;
                pointer-events: none;
                display: flex;
                height: 100vh;
                width: 100vw;
            }
            
            .left-panel {
                flex: 1;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                padding: 20px;
            }
            
            .right-panel {
                width: 300px;
                background: rgba(20, 20, 20, 0.85);
                backdrop-filter: blur(10px);
                border-left: 1px solid #333;
                padding: 20px;
                display: flex;
                flex-direction: column;
                pointer-events: auto;
                height: 100%;
                overflow-y: auto;
            }
            
            .pointer-events-auto {
                pointer-events: auto;
            }
            
            /* Scoreboard */
            .scoreboard {
                background: rgba(20, 20, 20, 0.85);
                backdrop-filter: blur(10px);
                border: 1px solid #333;
                border-radius: 15px;
                padding: 15px 30px;
                display: flex;
                flex-direction: column;
                align-items: center;
                align-self: center; /* Center horizontally in left panel */
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                max-width: 600px;
                width: 100%;
            }
            
            .scoreboard h1 {
                font-family: 'Orbitron', sans-serif;
                font-size: 1.5rem;
                letter-spacing: 4px;
                color: #aaa;
                margin-bottom: 10px;
                text-transform: uppercase;
            }
            
            .totals {
                display: flex;
                gap: 40px;
                justify-content: center;
                width: 100%;
            }
            
            .total-display {
                text-align: center;
            }
            
            .total-value {
                font-family: 'Orbitron', sans-serif;
                font-size: 3rem;
                font-weight: 700;
                color: #ff6b35;
                text-shadow: 0 0 15px rgba(255, 107, 53, 0.5);
                line-height: 1;
            }
            
            .total-unit {
                color: #888;
                font-weight: 700;
                font-size: 1rem;
            }

            /* Controls Panel (Bottom) */
            .controls-panel {
                background: rgba(20, 20, 20, 0.9);
                backdrop-filter: blur(10px);
                border: 1px solid #333;
                padding: 20px;
                border-radius: 20px;
                display: flex;
                flex-direction: column;
                gap: 20px;
                margin-top: auto; /* Push to bottom */
                max-width: 800px;
                align-self: center;
                width: 100%;
            }
            
            .bar-selector {
                display: flex;
                justify-content: center;
                gap: 20px;
            }
            
            .btn {
                background: #333;
                border: 1px solid #555;
                color: #fff;
                padding: 12px 24px;
                border-radius: 8px;
                font-family: 'Orbitron', sans-serif;
                cursor: pointer;
                transition: all 0.2s;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .btn:hover { background: #444; border-color: #777; }
            .btn:active { transform: translateY(2px); }
            
            .btn.active {
                background: linear-gradient(135deg, #ff6b35, #d84315);
                border-color: #ff6b35;
                box-shadow: 0 0 15px rgba(255, 107, 53, 0.4);
            }
            
            .btn-clear {
                background: #d32f2f;
                border-color: #b71c1c;
            }
            .btn-clear:hover { background: #e57373; }

            .plate-inventory {
                display: flex;
                justify-content: center;
                gap: 40px;
                flex-wrap: wrap;
            }
            
            .inventory-section {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 10px;
            }
            
            .inv-header {
                color: #888;
                font-family: 'Rajdhani', sans-serif;
                font-weight: 700;
                letter-spacing: 2px;
            }
            
            .plate-grid {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .inv-plate {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                border: 2px solid rgba(255,255,255,0.2);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 0.8rem;
                cursor: pointer;
                box-shadow: 0 4px 8px rgba(0,0,0,0.5);
                transition: transform 0.2s;
            }
            
            .inv-plate:hover { transform: scale(1.1); box-shadow: 0 6px 12px rgba(0,0,0,0.7); }
            .inv-plate:active { transform: scale(0.95); }
            
            .inv-plate span { font-size: 0.6rem; opacity: 0.7; }
            
            /* Plate Colors */
            .p-red { background: linear-gradient(135deg, #d32f2f, #b71c1c); border-color: #e57373; }
            .p-blue { background: linear-gradient(135deg, #1976d2, #0d47a1); border-color: #64b5f6; }
            .p-yellow { background: linear-gradient(135deg, #fbc02d, #f57f17); border-color: #fff176; color: #333; }
            .p-green { background: linear-gradient(135deg, #388e3c, #1b5e20); border-color: #81c784; }
            .p-white { background: linear-gradient(135deg, #e0e0e0, #9e9e9e); border-color: #fff; color: #333; }
            .p-black { background: linear-gradient(135deg, #424242, #212121); border-color: #616161; }

            /* Right Panel - Breakdown Table */
            .breakdown-title {
                font-family: 'Orbitron', sans-serif;
                font-size: 1.2rem;
                color: #ff6b35;
                margin-bottom: 20px;
                text-align: center;
                letter-spacing: 2px;
            }
            
            .breakdown-table {
                width: 100%;
                border-collapse: collapse;
            }
            
            .breakdown-table th {
                text-align: left;
                color: #888;
                border-bottom: 1px solid #444;
                padding: 10px 5px;
                font-size: 0.9rem;
            }
            
            .breakdown-table td {
                padding: 10px 5px;
                border-bottom: 1px solid #333;
                font-size: 1rem;
            }
            
            .row-plate {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .mini-plate {
                width: 15px;
                height: 15px;
                border-radius: 50%;
                display: inline-block;
            }

            .loading-overlay {
                position: fixed;
                top: 0; left: 0; right: 0; bottom: 0;
                background: #000;
                z-index: 100;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #ff6b35;
                font-family: 'Orbitron', sans-serif;
                font-size: 2rem;
                transition: opacity 0.5s;
                pointer-events: none;
            }
            .hidden { opacity: 0; }
            
            .instruction-toast {
                position: absolute;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0,0,0,0.7);
                padding: 10px 20px;
                border-radius: 20px;
                font-size: 0.9rem;
                color: #aaa;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.5s;
            }
            
        </style>
    </head>
    <body>
        <div class="loading-overlay" id="loader">LOADING 3D ASSETS...</div>
        
        <div id="canvas-container"></div>
        
        <div class="ui-container">
            <div class="instruction-toast" id="toast">Plate Removed</div>
            
            <div class="left-panel">
                <!-- Scoreboard -->
                <div class="scoreboard pointer-events-auto">
                    <h1>BARLOAD 3D</h1>
                    <div class="totals">
                        <div class="total-display">
                            <div class="total-value" id="lbs-total">45.0</div>
                            <div class="total-unit">LBS</div>
                        </div>
                        <div class="total-display">
                            <div class="total-value" id="kg-total">20.4</div>
                            <div class="total-unit">KG</div>
                        </div>
                    </div>
                </div>
                
                <!-- Controls -->
                <div class="controls-panel pointer-events-auto">
                    <div class="bar-selector">
                        <button class="btn btn-clear" onclick="window.app.clearBar()">CLEAR BAR</button>
                        <button class="btn active" id="btn-45" onclick="window.app.setBar(45, 'lbs')">45 LB BAR</button>
                        <button class="btn" id="btn-20" onclick="window.app.setBar(20, 'kg')">20 KG BAR</button>
                    </div>
                    
                    <div class="plate-inventory">
                        <div class="inventory-section">
                            <div class="inv-header">LBS PLATES</div>
                            <div class="plate-grid">
                                <div class="inv-plate p-red" onclick="window.app.addPlate(55, 'lbs', 'red')">55<span>LB</span></div>
                                <div class="inv-plate p-blue" onclick="window.app.addPlate(45, 'lbs', 'blue')">45<span>LB</span></div>
                                <div class="inv-plate p-yellow" onclick="window.app.addPlate(35, 'lbs', 'yellow')">35<span>LB</span></div>
                                <div class="inv-plate p-green" onclick="window.app.addPlate(25, 'lbs', 'green')">25<span>LB</span></div>
                                <div class="inv-plate p-white" onclick="window.app.addPlate(10, 'lbs', 'white')">10<span>LB</span></div>
                                <div class="inv-plate p-black" onclick="window.app.addPlate(5, 'lbs', 'black')">5<span>LB</span></div>
                                <div class="inv-plate p-black" onclick="window.app.addPlate(2.5, 'lbs', 'black')">2.5<span>LB</span></div>
                            </div>
                        </div>
                        
                        <div class="inventory-section">
                            <div class="inv-header">KG PLATES</div>
                            <div class="plate-grid">
                                <div class="inv-plate p-red" onclick="window.app.addPlate(25, 'kg', 'red')">25<span>KG</span></div>
                                <div class="inv-plate p-blue" onclick="window.app.addPlate(20, 'kg', 'blue')">20<span>KG</span></div>
                                <div class="inv-plate p-yellow" onclick="window.app.addPlate(15, 'kg', 'yellow')">15<span>KG</span></div>
                                <div class="inv-plate p-green" onclick="window.app.addPlate(10, 'kg', 'green')">10<span>KG</span></div>
                                <div class="inv-plate p-white" onclick="window.app.addPlate(5, 'kg', 'white')">5<span>KG</span></div>
                                <div class="inv-plate p-black" onclick="window.app.addPlate(2.5, 'kg', 'black')">2.5<span>KG</span></div>
                                <div class="inv-plate p-black" onclick="window.app.addPlate(1.25, 'kg', 'black')">1.25<span>KG</span></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="right-panel">
                <h2 class="breakdown-title">LOAD BREAKDOWN</h2>
                <table class="breakdown-table">
                    <thead>
                        <tr>
                            <th>PLATE</th>
                            <th>QTY</th>
                        </tr>
                    </thead>
                    <tbody id="breakdown-body">
                        <!-- Filled by JS -->
                    </tbody>
                </table>
            </div>
        </div>

        <script type="module">
            import * as THREE from 'three';
            import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

            class BarLoad3D {
                constructor() {
                    this.scene = null;
                    this.camera = null;
                    this.renderer = null;
                    this.controls = null;
                    this.raycaster = new THREE.Raycaster();
                    this.mouse = new THREE.Vector2();
                    this.barGroup = new THREE.Group();
                    this.platesLeft = [];
                    this.platesRight = [];
                    
                    this.state = {
                        barWeight: 45,
                        barUnit: 'lbs',
                        plates: []
                    };
                    
                    this.materials = {};
                    this.textures = {}; // Cache for label textures
                    
                    this.init();
                    this.animate();
                    
                    // Raycasting
                    window.addEventListener('click', (e) => this.onMouseClick(e));
                }
                
                init() {
                    // Scene Setup
                    this.scene = new THREE.Scene();
                    this.scene.background = new THREE.Color(0x222222);
                    
                    // Camera
                    this.camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
                    this.camera.position.set(0, 2, 4); 
                    
                    // Renderer
                    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
                    this.renderer.setSize(window.innerWidth, window.innerHeight);
                    this.renderer.shadowMap.enabled = true;
                    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
                    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
                    this.renderer.toneMappingExposure = 1.2;
                    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
                    document.getElementById('canvas-container').appendChild(this.renderer.domElement);
                    
                    // Controls
                    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
                    this.controls.enableDamping = true;
                    this.controls.minDistance = 2;
                    this.controls.maxDistance = 10;
                    this.controls.maxPolarAngle = Math.PI / 2;
                    
                    // Lighting
                    const ambient = new THREE.AmbientLight(0xffffff, 1.0);
                    this.scene.add(ambient);
                    
                    // Key Light
                    const mainSpot = new THREE.SpotLight(0xffffff, 20);
                    mainSpot.position.set(5, 8, 5);
                    mainSpot.angle = Math.PI / 4;
                    mainSpot.penumbra = 0.5;
                    mainSpot.castShadow = true;
                    this.scene.add(mainSpot);
                    
                    // Fill Light
                    const fillLight = new THREE.DirectionalLight(0xeef4ff, 3);
                    fillLight.position.set(-5, 3, -5);
                    this.scene.add(fillLight);
                    
                    // Rim Light
                    const rimLight = new THREE.DirectionalLight(0xffaa00, 2);
                    rimLight.position.set(0, 2, -5);
                    this.scene.add(rimLight);
                    
                    // Floor
                    const floorGeom = new THREE.PlaneGeometry(50, 50);
                    const floorMat = new THREE.MeshStandardMaterial({ 
                        color: 0x1a1a1a, 
                        roughness: 0.8, 
                        metalness: 0.1 
                    });
                    const floor = new THREE.Mesh(floorGeom, floorMat);
                    floor.rotation.x = -Math.PI / 2;
                    floor.position.y = -0.6;
                    floor.receiveShadow = true;
                    this.scene.add(floor);
                    
                    // Materials Init
                    this.initMaterials();
                    
                    // Build Barbell
                    this.buildBarbell();
                    this.scene.add(this.barGroup);
                    
                    // Handle Resize
                    window.addEventListener('resize', () => {
                        this.camera.aspect = window.innerWidth / window.innerHeight;
                        this.camera.updateProjectionMatrix();
                        this.renderer.setSize(window.innerWidth, window.innerHeight);
                    });
                    
                    // Hide loader
                    setTimeout(() => {
                        document.getElementById('loader').classList.add('hidden');
                    }, 1000);
                }
                
                initMaterials() {
                    this.materials.chrome = new THREE.MeshStandardMaterial({
                        color: 0xffffff,
                        metalness: 0.9,
                        roughness: 0.1,
                    });
                    
                    this.materials.blackOxide = new THREE.MeshStandardMaterial({
                        color: 0x333333,
                        metalness: 0.6,
                        roughness: 0.4,
                    });
                    
                    // Rubber Plates defined as functions of color
                    this.createPlateMaterial = (colorHex) => {
                        return new THREE.MeshStandardMaterial({
                            color: colorHex,
                            metalness: 0.1,
                            roughness: 0.4, // Rubbery
                        });
                    }
                    
                    this.materials.red = this.createPlateMaterial(0xd32f2f);
                    this.materials.blue = this.createPlateMaterial(0x1976d2);
                    this.materials.yellow = this.createPlateMaterial(0xfbc02d);
                    this.materials.green = this.createPlateMaterial(0x388e3c);
                    this.materials.white = this.createPlateMaterial(0xe0e0e0);
                    this.materials.black = this.createPlateMaterial(0x212121);
                }
                
                buildBarbell() {
                    // Same as before
                    const shaftGeom = new THREE.CylinderGeometry(0.014, 0.014, 1.31, 32); 
                    const shaft = new THREE.Mesh(shaftGeom, this.materials.blackOxide);
                    shaft.rotation.z = Math.PI / 2;
                    shaft.castShadow = true;
                    
                    const sleeveGeom = new THREE.CylinderGeometry(0.025, 0.025, 0.415, 32);
                    
                    const sleeveLeft = new THREE.Mesh(sleeveGeom, this.materials.chrome);
                    sleeveLeft.rotation.z = Math.PI / 2;
                    sleeveLeft.position.x = -0.8625;
                    sleeveLeft.castShadow = true;
                    
                    const sleeveRight = new THREE.Mesh(sleeveGeom, this.materials.chrome);
                    sleeveRight.rotation.z = Math.PI / 2;
                    sleeveRight.position.x = 0.8625;
                    sleeveRight.castShadow = true;
                    
                    const collarGeom = new THREE.CylinderGeometry(0.035, 0.035, 0.03, 32);
                    const collarLeft = new THREE.Mesh(collarGeom, this.materials.chrome);
                    collarLeft.rotation.z = Math.PI / 2;
                    collarLeft.position.x = -0.67;
                    collarLeft.castShadow = true;
                    
                    const collarRight = new THREE.Mesh(collarGeom, this.materials.chrome);
                    collarRight.rotation.z = Math.PI / 2;
                    collarRight.position.x = 0.67;
                    collarRight.castShadow = true;
                    
                    this.barGroup.add(shaft, sleeveLeft, sleeveRight, collarLeft, collarRight);
                }
                
                // --- Text Label Generation ---
                createLabelTexture(text, fg="white") {
                     const canvas = document.createElement('canvas');
                     canvas.width = 512;
                     canvas.height = 512;
                     const ctx = canvas.getContext('2d');
                     
                     // Helper: Draw Circular Text
                     ctx.fillStyle = fg;
                     ctx.font = "bold 80px Arial";
                     ctx.textAlign = "center";
                     ctx.textBaseline = "middle";
                     
                     // Top text
                     ctx.save();
                     ctx.translate(256, 120);
                     ctx.rotate(Math.PI);
                     ctx.fillText(text, 0, 0);
                     ctx.restore();
                     
                     // Bottom text
                     ctx.save();
                     ctx.translate(256, 392);
                     ctx.fillText(text, 0, 0);
                     ctx.restore();
                     
                     // Inner Ring Line
                     ctx.strokeStyle = "rgba(255,255,255,0.3)";
                     ctx.lineWidth = 10;
                     ctx.beginPath();
                     ctx.arc(256, 256, 180, 0, Math.PI*2);
                     ctx.stroke();

                     const tex = new THREE.CanvasTexture(canvas);
                     tex.anisotropy = this.renderer.capabilities.getMaxAnisotropy();
                     return tex;
                }

                createVisualPlateMesh(weight, unit, colorName) {
                    let diameter = 0.45; 
                    let thickness = 0.05; 
                    
                    if (unit === 'lbs') {
                        if (weight >= 45) { diameter = 0.45; thickness = 0.06; }
                        else if (weight >= 35) { diameter = 0.35; thickness = 0.05; }
                        else if (weight >= 25) { diameter = 0.28; thickness = 0.04; }
                        else if (weight >= 10) { diameter = 0.22; thickness = 0.03; }
                        else { diameter = 0.16; thickness = 0.02; }
                    } else {
                        if (weight >= 20) { diameter = 0.45; thickness = 0.055; }
                        else if (weight >= 15) { diameter = 0.38; thickness = 0.05; }
                        else if (weight >= 10) { diameter = 0.32; thickness = 0.035; } 
                        else { diameter = 0.20; thickness = 0.02; }
                    }
                    
                    // Base material color
                    const baseMat = this.materials[colorName] || this.materials.black;
                    
                    // Create Label Texture - Always White Text
                    const labelText = `${weight} ${unit.toUpperCase()}`;
                    const labelTex = this.createLabelTexture(labelText, 'white');
                    
                    // We want the text ON TOP of the color.
                    // This is tricky with simple map because white text + red color = red text.
                    // Instead, we use the texture as an alpha map for a white material layered on top?
                    // Or simpler: Use a separate transparent plane for text?
                    // EASIEST: Just map the texture to a new material that ignores the base color?
                    // NO: The side needs to be red. The face needs to be red WITH white text.
                    
                    // SOLUTION: The face material should use the plate color, but mix in the white text?
                    // Standard material map multiplies color. 
                    // If we want white text, the label texture should be white on transparent.
                    // But standard material will multiply that white by the material color (e.g. red), making it red text.
                    
                    // ALTERNATIVE: Use 2 meshes? 
                    // 1. Base cylinder (Color)
                    // 2. Text cylinder (Transparent + White Text decal) scaling slightly z-fighting risk.
                    
                    // BETTER: Use Canvas to draw the background color AND the text?
                    // Yes. We can paint the canvas the plate color, then draw white text.
                    // Then use that texture as the map, and set material color to white.
                    
                    // Let's create a specific color texture for this plate
                    const canvas = document.createElement('canvas');
                    canvas.width = 512;
                    canvas.height = 512;
                    const ctx = canvas.getContext('2d');
                    
                    // Fill with plate color
                    // Need hex color string
                    let colorHex = '#212121';
                    if(colorName === 'red') colorHex = '#d32f2f';
                    else if(colorName === 'blue') colorHex = '#1976d2';
                    else if(colorName === 'yellow') colorHex = '#fbc02d';
                    else if(colorName === 'green') colorHex = '#388e3c';
                    else if(colorName === 'white') colorHex = '#e0e0e0';
                    
                    ctx.fillStyle = colorHex;
                    ctx.fillRect(0,0,512,512);
                    
                    // Text
                    ctx.fillStyle = 'white';
                    ctx.font = "bold 80px Arial";
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    
                    // Top
                    ctx.save();
                    ctx.translate(256, 120);
                    ctx.rotate(Math.PI);
                    ctx.fillText(labelText, 0, 0);
                    ctx.restore();
                    
                    // Bottom
                    ctx.save();
                    ctx.translate(256, 392);
                    ctx.fillText(labelText, 0, 0);
                    ctx.restore();
                    
                    // Ring
                    ctx.strokeStyle = "rgba(255,255,255,0.3)";
                    ctx.lineWidth = 10;
                    ctx.beginPath();
                    ctx.arc(256, 256, 180, 0, Math.PI*2);
                    ctx.stroke();
                    
                    const tex = new THREE.CanvasTexture(canvas);
                    tex.anisotropy = this.renderer.capabilities.getMaxAnisotropy();
                    tex.colorSpace = THREE.SRGBColorSpace;
                    
                    // Face Material: White base color (so texture shows exactly) + Map
                    const faceMat = new THREE.MeshStandardMaterial({
                        map: tex,
                        roughness: 0.4,
                        metalness: 0.1
                    });
                    
                    // Side Material: Just the solid color material
                    const sideMat = baseMat;
                    
                    const materials = [sideMat, faceMat, faceMat];
                    
                    const geometry = new THREE.CylinderGeometry(diameter/2, diameter/2, thickness, 48);
                    const mesh = new THREE.Mesh(geometry, materials);
                    mesh.rotation.z = Math.PI / 2;
                    mesh.castShadow = true;
                    
                    // OUTLINE - Restored for visibility
                    const edges = new THREE.EdgesGeometry(geometry);
                    const lineMat = new THREE.LineBasicMaterial({ color: 0x000000, linewidth: 1, transparent: true, opacity: 0.5 });
                    const outline = new THREE.LineSegments(edges, lineMat);
                    mesh.add(outline); 
                    
                    return { mesh, thickness };
                }

                addPlateVisuals(plateIndex) {
                    const p = this.state.plates[plateIndex];
                    const visual = this.createVisualPlateMesh(p.weight, p.unit, p.color);
                    
                    visual.mesh.userData = { plateIndex: plateIndex };
                    
                    let offsetBase = 0.69;
                    
                    // Left Plate
                    const plateL = visual.mesh.clone();
                    plateL.userData = { plateIndex: plateIndex, side: 'left' };
                    
                    let stackHeightL = this.platesLeft.reduce((acc, obj) => acc + obj.thickness, 0);
                    plateL.position.x = -(offsetBase + stackHeightL + visual.thickness/2);
                    
                    this.platesLeft.push({ mesh: plateL, thickness: visual.thickness, plateIndex: plateIndex });
                    this.barGroup.add(plateL);
                    
                    // Right Plate
                    const plateR = visual.mesh.clone();
                    plateR.userData = { plateIndex: plateIndex, side: 'right' };
                    
                    let stackHeightR = this.platesRight.reduce((acc, obj) => acc + obj.thickness, 0);
                    plateR.position.x = (offsetBase + stackHeightR + visual.thickness/2);
                    
                    this.platesRight.push({ mesh: plateR, thickness: visual.thickness, plateIndex: plateIndex });
                    this.barGroup.add(plateR);
                }
                
                rebuildVisuals() {
                    this.platesLeft.forEach(p => this.barGroup.remove(p.mesh));
                    this.platesRight.forEach(p => this.barGroup.remove(p.mesh));
                    this.platesLeft = [];
                    this.platesRight = [];
                    
                    this.state.plates.forEach((p, index) => {
                        this.addPlateVisuals(index);
                    });
                }
                
                onMouseClick(event) {
                    this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
                    this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
                    this.raycaster.setFromCamera(this.mouse, this.camera);
                    
                    const intersects = this.raycaster.intersectObjects(this.barGroup.children, false);
                    
                    if (intersects.length > 0) {
                        const object = intersects[0].object;
                        if (object.userData && object.userData.plateIndex !== undefined) {
                            this.removePlate(object.userData.plateIndex);
                        }
                    }
                }
                
                removePlate(index) {
                    this.state.plates.splice(index, 1);
                    this.rebuildVisuals();
                    this.updateScoreboard();
                    this.updateToast('Plate pair removed');
                }
                
                updateToast(msg) {
                    const toast = document.getElementById('toast');
                    toast.innerText = msg;
                    toast.style.opacity = 1;
                    setTimeout(() => { toast.style.opacity = 0; }, 2000);
                }
                
                animate() {
                    requestAnimationFrame(() => this.animate());
                    this.controls.update();
                    this.renderer.render(this.scene, this.camera);
                }
                
                // --- Public API ---
                
                setBar(weight, unit) {
                    this.state.barWeight = weight;
                    this.state.barUnit = unit;
                    
                    document.getElementById('btn-45').classList.remove('active');
                    document.getElementById('btn-20').classList.remove('active');
                    if(unit === 'lbs') document.getElementById('btn-45').classList.add('active');
                    else document.getElementById('btn-20').classList.add('active');
                    
                    this.updateScoreboard();
                }
                
                addPlate(weight, unit, color) {
                    this.state.plates.push({weight, unit, color});
                    this.addPlateVisuals(this.state.plates.length - 1);
                    this.updateScoreboard();
                }
                
                clearBar() {
                    this.state.plates = [];
                    this.rebuildVisuals();
                    this.updateScoreboard();
                }
                
                updateScoreboard() {
                   const KG_TO_LBS = 2.20462;
                   let totalLbs = 0;
                   let totalKg = 0;
                   
                   if(this.state.barUnit === 'lbs') {
                       totalLbs += this.state.barWeight;
                       totalKg += this.state.barWeight / KG_TO_LBS;
                   } else {
                       totalKg += this.state.barWeight;
                       totalLbs += this.state.barWeight * KG_TO_LBS;
                   }
                   
                   const counts = {}; 
                   
                   this.state.plates.forEach(p => {
                       let w = p.weight * 2; 
                       if(p.unit === 'lbs') {
                           totalLbs += w;
                           totalKg += w / KG_TO_LBS;
                       } else {
                           totalKg += w;
                           totalLbs += w * KG_TO_LBS;
                       }
                       
                       const key = `${p.weight} ${p.unit}`;
                       counts[key] = (counts[key] || 0) + 1; 
                   });
                   
                   document.getElementById('lbs-total').innerText = totalLbs.toFixed(1);
                   document.getElementById('kg-total').innerText = totalKg.toFixed(1);
                   
                   this.renderBreakdown(counts);
                }
                
                renderBreakdown(counts) {
                    const tbody = document.getElementById('breakdown-body');
                    tbody.innerHTML = '';
                    
                    const trBar = document.createElement('tr');
                    trBar.innerHTML = `
                        <td>${this.state.barWeight} ${this.state.barUnit} Bar</td>
                        <td>1</td>
                    `;
                    tbody.appendChild(trBar);
                    
                    for (const [key, count] of Object.entries(counts)) {
                        const tr = document.createElement('tr');
                        const totalPlates = count * 2; 
                        
                        let colorClass = 'p-black';
                        if(key.includes('55') || key.includes('25 kg')) colorClass = 'p-red';
                        else if(key.includes('45') || key.includes('20 kg')) colorClass = 'p-blue';
                        else if(key.includes('35') || key.includes('15 kg')) colorClass = 'p-yellow';
                        else if(key.includes('25') || key.includes('10 kg')) colorClass = 'p-green';
                        else if(key.includes('10 lb') || key.includes('5 kg')) colorClass = 'p-white';
                        
                        tr.innerHTML = `
                            <td><div class="row-plate">
                                <span class="mini-plate inv-plate ${colorClass}" style="width:15px;height:15px;border:none;"></span>
                                ${key}
                            </div></td>
                            <td>x ${totalPlates}</td>
                        `;
                        tbody.appendChild(tr);
                    }
                }
            }

            // Init App
            window.onload = () => {
                window.app = new BarLoad3D();
            };
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
