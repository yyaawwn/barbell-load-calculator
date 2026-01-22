from flask import Flask

app = Flask(__name__)

@app.route('/')
def barbell_calculator():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BarLoad - Barbell Calculator</title>
        <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Rajdhani', sans-serif;
                background: linear-gradient(135deg, #121212 0%, #1e1e1e 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
                color: #e0e0e0;
            }
            
            .container {
                max-width: 1000px;
                width: 100%;
                background: #222;
                border: 1px solid #333;
                border-radius: 12px;
                padding: 2rem;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7);
            }
            
            /* Scoreboard */
            .scoreboard {
                background: #1a1a1a;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 30px;
                text-align: center;
                border: 1px solid #333;
                box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
            }
            
            .scoreboard h1 {
                font-family: 'Orbitron', sans-serif;
                font-size: 2.2rem;
                letter-spacing: 4px;
                color: #ccc;
                text-transform: uppercase;
                margin-bottom: 25px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.5);
            }
            
            .totals {
                display: flex;
                justify-content: center;
                gap: 40px;
                margin-bottom: 25px;
            }
            
            .total-display {
                background: #000;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 10px 25px;
                min-width: 200px;
                display: flex;
                align-items: baseline;
                justify-content: center;
                box-shadow: inset 0 0 15px rgba(255, 107, 53, 0.1);
            }
            
            .total-value {
                font-family: 'Orbitron', sans-serif;
                font-size: 3.5rem;
                font-weight: 700;
                color: #ff6b35;
                text-shadow: 0 0 15px rgba(255, 107, 53, 0.4);
                line-height: 1;
            }
            
            .total-unit {
                font-family: 'Rajdhani', sans-serif;
                font-size: 1.2rem;
                color: #666;
                margin-left: 8px;
                font-weight: 700;
            }
            
            .clear-btn {
                background: linear-gradient(to bottom, #444, #333);
                border: 1px solid #555;
                color: #ccc;
                padding: 10px 30px;
                border-radius: 4px;
                font-size: 0.9rem;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.2s ease;
                font-family: 'Orbitron', sans-serif;
                letter-spacing: 1px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }
            
            .clear-btn:hover {
                background: linear-gradient(to bottom, #555, #444);
                color: #fff;
                border-color: #777;
            }
            
            .clear-btn:active {
                transform: translateY(1px);
                box-shadow: 0 1px 2px rgba(0,0,0,0.3);
            }
            
            /* Realistic Barbell Visualizer */
            .visualizer {
                background: #181818;
                border-radius: 8px;
                padding: 60px 20px;
                margin-bottom: 30px;
                border: 1px solid #333;
                min-height: 250px;
                position: relative;
                overflow-x: hidden; /* Prevent scrollbar during animation */
                display: flex;
                justify-content: center;
                align-items: center;
                box-shadow: inset 0 0 50px rgba(0,0,0,0.8);
            }
            
            /* The Barbell Assembly */
            .barbell-assembly {
                position: relative;
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 200px;
            }

            /* Central Shaft */
            .shaft {
                height: 12px;
                width: 100%; /* Spans full width initially, masked by plates */
                max-width: 1100px; 
                background: linear-gradient(to bottom, 
                    #666 0%, 
                    #eee 40%, 
                    #ccc 50%, 
                    #999 60%, 
                    #444 100%
                );
                position: absolute;
                z-index: 1;
                border-radius: 2px;
                box-shadow: 0 5px 10px rgba(0,0,0,0.5);
            }
            
            /* Knurling pattern overlay on shaft */
            .shaft::after {
                content: '';
                position: absolute;
                top: 0;
                left: 20%;
                right: 20%;
                bottom: 0;
                background-image: repeating-linear-gradient(
                    45deg,
                    transparent,
                    transparent 2px,
                    rgba(0,0,0,0.1) 2px,
                    rgba(0,0,0,0.1) 4px
                ), repeating-linear-gradient(
                    -45deg,
                    transparent,
                    transparent 2px,
                    rgba(0,0,0,0.1) 2px,
                    rgba(0,0,0,0.1) 4px
                );
                opacity: 0.6;
            }
            
            /* Sleeves */
            .sleeve-container-left, .sleeve-container-right {
                position: absolute;
                height: 20px;
                width: 320px; /* Typical sleeve length relative */
                background: linear-gradient(to bottom, 
                    #888 0%, 
                    #fff 40%, 
                    #ccc 50%, 
                    #999 60%, 
                    #555 100%
                );
                z-index: 2;
                display: flex;
                align-items: center;
            }

            .sleeve-container-left {
                right: 50%;
                margin-right: 60px; /* Half of center gap */
                flex-direction: row-reverse; /* Load from collar outwards */
                border-radius: 2px 0 0 2px;
            }
            
            .sleeve-container-right {
                left: 50%;
                margin-left: 60px; /* Half of center gap */
                flex-direction: row; /* Load from collar outwards */
                border-radius: 0 2px 2px 0;
            }
            
            /* Collars */
            .collar {
                width: 15px;
                height: 30px;
                background: linear-gradient(to right, #333, #555, #333);
                border: 1px solid #222;
                box-shadow: 2px 0 5px rgba(0,0,0,0.5);
                z-index: 5;
                flex-shrink: 0;
            }
            
            /* Plate Styles (Side View) */
            .plate {
                z-index: 10;
                border-radius: 3px;
                margin: 0 1px; /* Tiny gap between plates */
                box-shadow: 
                    2px 0 4px rgba(0,0,0,0.5), 
                    inset 1px 1px 2px rgba(255,255,255,0.3),
                    inset -1px -1px 2px rgba(0,0,0,0.3);
                position: relative;
                flex-shrink: 0;
                transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                animation: slideOn 0.4s ease-out forwards;
            }
            
            @keyframes slideOn {
                from { opacity: 0; transform: scale(0.9) translateX(20px); }
                to { opacity: 1; transform: scale(1) translateX(0); }
            }
            
            /* Specific Plate Dimensions (Height = Diameter, Width = Thickness) */
            /* Using pixels for precise visual ratio */
            
            /* HEIGHTS (Diameter) */
            .h-large { height: 160px; } /* 45lb/20kg (Standard 450mm) */
            .h-med { height: 140px; }   /* 35lb/15kg */
            .h-small { height: 110px; } /* 25lb/10kg */
            .h-xs { height: 80px; }     /* 10lb/5kg */
            .h-xxs { height: 60px; }    /* 5lb/2.5kg */
            .h-micro { height: 45px; }  /* 2.5lb/1.25kg */
            
            /* WIDTHS (Thickness) */
            .w-thick { width: 35px; }   /* 45lb */
            .w-med-thick { width: 30px; } /* 35ld/20kg */
            .w-med { width: 22px; }     /* 25lb/15kg */
            .w-thin { width: 16px; }    /* 10lb/10kg */
            .w-slim { width: 12px; }    /* 5lb/5kg */
            .w-micro { width: 10px; }   /* 2.5lb */

            /* COLORS (Olympic Bumper Style) */
            .bg-red { 
                background: linear-gradient(to right, #b71c1c, #d32f2f 40%, #e57373 50%, #d32f2f 60%, #b71c1c); 
                border-left: 1px solid #8c1414;
                border-right: 1px solid #8c1414;
            }
            .bg-blue { 
                background: linear-gradient(to right, #0d47a1, #1976d2 40%, #64b5f6 50%, #1976d2 60%, #0d47a1);
                border-left: 1px solid #08367a;
                border-right: 1px solid #08367a;
            }
            .bg-yellow { 
                background: linear-gradient(to right, #f57f17, #fbc02d 40%, #fff176 50%, #fbc02d 60%, #f57f17);
                border-left: 1px solid #bc600c;
                border-right: 1px solid #bc600c;
            }
            .bg-green { 
                background: linear-gradient(to right, #1b5e20, #388e3c 40%, #81c784 50%, #388e3c 60%, #1b5e20);
                border-left: 1px solid #124016;
                border-right: 1px solid #124016;
            }
            .bg-white { 
                background: linear-gradient(to right, #616161, #9e9e9e 40%, #e0e0e0 50%, #9e9e9e 60%, #616161); /* Grey/White bumper look */
                border-left: 1px solid #4a4a4a;
                border-right: 1px solid #4a4a4a;
            }
             .bg-micro { 
                background: linear-gradient(to right, #212121, #424242 40%, #757575 50%, #424242 60%, #212121); /* Dark grey */
                border-left: 1px solid #000;
                border-right: 1px solid #000;
            }

            /* Inventory Styling updates */
            .inventory-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 20px;
            }
            
            .inv-col {
                background: #1a1a1a;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 15px;
            }
            
            .inv-header {
                text-align: center;
                color: #888;
                font-family: 'Orbitron', sans-serif;
                margin-bottom: 15px;
                font-size: 1rem;
                letter-spacing: 2px;
            }
            
            .plate-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
                gap: 12px;
                justify-items: center;
            }
            
            .inv-btn {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                border: none;
                color: white;
                font-weight: bold;
                font-family: 'Rajdhani', sans-serif;
                font-size: 1rem;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 4px 8px rgba(0,0,0,0.4);
                transition: transform 0.1s;
                text-shadow: 0 1px 2px rgba(0,0,0,0.8);
                position: relative;
            }
            
            .inv-btn span { font-size: 0.7rem; opacity: 0.8; }
            .inv-btn:active { transform: scale(0.95); }
            
            /* Button Colors (Face View) */
            .btn-red { background: radial-gradient(circle at 30% 30%, #e57373, #b71c1c); border: 2px solid #8c1414; }
            .btn-blue { background: radial-gradient(circle at 30% 30%, #64b5f6, #0d47a1); border: 2px solid #08367a; }
            .btn-yellow { background: radial-gradient(circle at 30% 30%, #fff176, #fbc02d); border: 2px solid #f57f17; color: #333; text-shadow: none; }
            .btn-green { background: radial-gradient(circle at 30% 30%, #81c784, #1b5e20); border: 2px solid #124016; }
            .btn-white { background: radial-gradient(circle at 30% 30%, #e0e0e0, #9e9e9e); border: 2px solid #757575; color: #333; text-shadow: none; }
            .btn-black { background: radial-gradient(circle at 30% 30%, #757575, #212121); border: 2px solid #000; }
            
            .inv-btn::after {
                content: '';
                position: absolute;
                width: 12px;
                height: 12px;
                background: #1a1a1a;
                border-radius: 50%;
                border: 2px solid rgba(255,255,255,0.1);
            }

            /* Bar Selection */
            .bar-select {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-top: 20px;
            }
            
            .bar-btn {
                padding: 20px;
                background: #252525;
                border: 2px solid #444;
                color: #888;
                font-family: 'Orbitron', sans-serif;
                font-size: 1.2rem;
                cursor: pointer;
                border-radius: 8px;
                transition: all 0.3s;
                text-transform: uppercase;
            }
            
            .bar-btn.active {
                border-color: #ff6b35;
                color: #fff;
                background: linear-gradient(135deg, #2a2a2a, #333);
                box-shadow: 0 0 15px rgba(255, 107, 53, 0.2);
            }

        </style>
    </head>
    <body>
        <div class="container">
            <!-- Scoreboard -->
            <div class="scoreboard">
                <h1>SCOREBOARD</h1>
                <div class="totals">
                    <div class="total-display">
                        <span class="total-value" id="lbs-total">45.0</span>
                        <span class="total-unit">LBS</span>
                    </div>
                    <div class="total-display">
                        <span class="total-value" id="kg-total">20.4</span>
                        <span class="total-unit">KG</span>
                    </div>
                </div>
                <button class="clear-btn" onclick="clearBar()">CLEAR BAR</button>
            </div>
            
            <!-- Realistic Barbell Visualizer -->
            <div class="visualizer">
                <div class="barbell-assembly">
                    <div class="shaft"></div>
                    
                    <!-- Left Sleeve -->
                    <div class="sleeve-container-left" id="sleeve-left">
                        <div class="collar"></div>
                        <!-- Plates go here via JS -->
                    </div>
                    
                    <!-- Right Sleeve -->
                    <div class="sleeve-container-right" id="sleeve-right">
                        <div class="collar"></div>
                        <!-- Plates go here via JS -->
                    </div>
                </div>
            </div>
            
            <!-- Plate Inventory -->
            <div class="inventory-container">
                <!-- LBS Plates -->
                <div class="inv-col">
                    <div class="inv-header">LBS PLATES</div>
                    <div class="plate-grid">
                        <button class="inv-btn btn-red" onclick="addPlate(55, 'lbs')">55<span>LBS</span></button>
                        <button class="inv-btn btn-blue" onclick="addPlate(45, 'lbs')">45<span>LBS</span></button>
                        <button class="inv-btn btn-yellow" onclick="addPlate(35, 'lbs')">35<span>LBS</span></button>
                        <button class="inv-btn btn-green" onclick="addPlate(25, 'lbs')">25<span>LBS</span></button>
                        <button class="inv-btn btn-white" onclick="addPlate(10, 'lbs')">10<span>LBS</span></button>
                        <button class="inv-btn btn-black" onclick="addPlate(5, 'lbs')">5<span>LBS</span></button>
                        <button class="inv-btn btn-black" onclick="addPlate(2.5, 'lbs')">2.5<span>LBS</span></button>
                    </div>
                </div>
                
                <!-- KG Plates -->
                <div class="inv-col">
                    <div class="inv-header">KG PLATES</div>
                    <div class="plate-grid">
                        <button class="inv-btn btn-red" onclick="addPlate(25, 'kg')">25<span>KG</span></button>
                        <button class="inv-btn btn-blue" onclick="addPlate(20, 'kg')">20<span>KG</span></button>
                        <button class="inv-btn btn-yellow" onclick="addPlate(15, 'kg')">15<span>KG</span></button>
                        <button class="inv-btn btn-green" onclick="addPlate(10, 'kg')">10<span>KG</span></button>
                        <button class="inv-btn btn-white" onclick="addPlate(5, 'kg')">5<span>KG</span></button>
                        <button class="inv-btn btn-black" onclick="addPlate(2.5, 'kg')">2.5<span>KG</span></button>
                        <button class="inv-btn btn-black" onclick="addPlate(1.25, 'kg')">1.25<span>KG</span></button>
                    </div>
                </div>
            </div>
            
            <!-- Bar Selection -->
            <div class="bar-select">
                <button class="bar-btn active" id="btn-45" onclick="setBar(45, 'lbs')">45 LB BARBELL</button>
                <button class="bar-btn" id="btn-20" onclick="setBar(20, 'kg')">20 KG BARBELL</button>
            </div>
        </div>
        
        <script>
            let currentBarWeight = 45;
            let currentBarUnit = 'lbs';
            let plates = []; // {weight: number, unit: 'lbs'|'kg'}
            
            const KG_TO_LBS = 2.20462;
            
            function setBar(weight, unit) {
                currentBarWeight = weight;
                currentBarUnit = unit;
                
                document.getElementById('btn-45').classList.remove('active');
                document.getElementById('btn-20').classList.remove('active');
                
                if(unit === 'lbs') {
                    document.getElementById('btn-45').classList.add('active');
                } else {
                    document.getElementById('btn-20').classList.add('active');
                }
                update();
            }
            
            function addPlate(weight, unit) {
                plates.push({weight, unit});
                update();
            }
            
            function clearBar() {
                plates = [];
                update();
            }
            
            function update() {
                // 1. Calculate Totals
                let totalLbs = 0;
                let totalKg = 0;
                
                // Base weight
                if(currentBarUnit === 'lbs') {
                    totalLbs += currentBarWeight;
                    totalKg += currentBarWeight / KG_TO_LBS;
                } else {
                    totalKg += currentBarWeight;
                    totalLbs += currentBarWeight * KG_TO_LBS;
                }
                
                // Plates (times 2 for both sides)
                plates.forEach(p => {
                    let w = p.weight;
                    if(p.unit === 'lbs') {
                        totalLbs += w * 2;
                        totalKg += (w * 2) / KG_TO_LBS;
                    } else {
                        totalKg += w * 2;
                        totalLbs += (w * 2) * KG_TO_LBS;
                    }
                });
                
                document.getElementById('lbs-total').innerText = totalLbs.toFixed(1);
                document.getElementById('kg-total').innerText = totalKg.toFixed(1);
                
                // 2. Render Visuals
                renderPlates();
            }
            
            function getPlateClass(weight, unit) {
                // Map weight to size classes
                // Returns [heightClass, widthClass, colorClass]
                
                let h = 'h-med';
                let w = 'w-med';
                let c = 'bg-black';
                
                if(unit === 'lbs') {
                    // LBS mapping
                    if(weight >= 55) { h='h-large'; w='w-thick'; c='bg-red'; }
                    else if(weight >= 45) { h='h-large'; w='w-thick'; c='bg-blue'; }
                    else if(weight >= 35) { h='h-med'; w='w-med-thick'; c='bg-yellow'; }
                    else if(weight >= 25) { h='h-small'; w='w-med'; c='bg-green'; }
                    else if(weight >= 10) { h='h-xs'; w='w-thin'; c='bg-white'; }
                    else if(weight >= 5) { h='h-xxs'; w='w-slim'; c='bg-micro'; }
                    else { h='h-micro'; w='w-micro'; c='bg-micro'; }
                } else {
                    // KG mapping
                    if(weight >= 25) { h='h-large'; w='w-thick'; c='bg-red'; }
                    else if(weight >= 20) { h='h-large'; w='w-thick'; c='bg-blue'; }
                    else if(weight >= 15) { h='h-med'; w='w-med-thick'; c='bg-yellow'; }
                    else if(weight >= 10) { h='h-small'; w='w-med'; c='bg-green'; }
                    else if(weight >= 5) { h='h-xs'; w='w-thin'; c='bg-white'; }
                    else if(weight >= 2.5) { h='h-xxs'; w='w-slim'; c='bg-micro'; }
                    else { h='h-micro'; w='w-micro'; c='bg-micro'; }
                }
                return `${h} ${w} ${c}`;
            }
            
            function renderPlates() {
                const sl = document.getElementById('sleeve-left');
                const sr = document.getElementById('sleeve-right');
                
                // Keep collar
                sl.innerHTML = '<div class="collar"></div>';
                sr.innerHTML = '<div class="collar"></div>';
                
                plates.forEach(p => {
                    let classes = getPlateClass(p.weight, p.unit);
                    
                    let divL = document.createElement('div');
                    divL.className = 'plate ' + classes;
                    sl.appendChild(divL);
                    
                    let divR = document.createElement('div');
                    divR.className = 'plate ' + classes;
                    sr.appendChild(divR);
                });
            }
            
            // Init
            update();
            
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
