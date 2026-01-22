from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def calculator():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calculator - Flask App</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', sans-serif;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                overflow: hidden;
            }
            
            .circles {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                z-index: -1;
            }
            
            .circles li {
                position: absolute;
                display: block;
                list-style: none;
                width: 20px;
                height: 20px;
                background: rgba(255, 255, 255, 0.2);
                animation: animate 25s linear infinite;
                bottom: -150px;
            }
            
            .circles li:nth-child(1) { left: 25%; width: 80px; height: 80px; animation-delay: 0s; }
            .circles li:nth-child(2) { left: 10%; width: 20px; height: 20px; animation-delay: 2s; animation-duration: 12s; }
            .circles li:nth-child(3) { left: 70%; width: 20px; height: 20px; animation-delay: 4s; }
            .circles li:nth-child(4) { left: 40%; width: 60px; height: 60px; animation-delay: 0s; animation-duration: 18s; }
            .circles li:nth-child(5) { left: 65%; width: 20px; height: 20px; animation-delay: 0s; }
            .circles li:nth-child(6) { left: 75%; width: 110px; height: 110px; animation-delay: 3s; }
            .circles li:nth-child(7) { left: 35%; width: 150px; height: 150px; animation-delay: 7s; }
            .circles li:nth-child(8) { left: 50%; width: 25px; height: 25px; animation-delay: 15s; animation-duration: 45s; }
            .circles li:nth-child(9) { left: 20%; width: 15px; height: 15px; animation-delay: 2s; animation-duration: 35s; }
            .circles li:nth-child(10) { left: 85%; width: 150px; height: 150px; animation-delay: 0s; animation-duration: 11s; }
            
            @keyframes animate {
                0% {
                    transform: translateY(0) rotate(0deg);
                    opacity: 1;
                    border-radius: 0;
                }
                100% {
                    transform: translateY(-1000px) rotate(720deg);
                    opacity: 0;
                    border-radius: 50%;
                }
            }
            
            .calculator {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                padding: 2rem;
                animation: fadeIn 0.8s ease-in;
                width: 380px;
            }
            
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: scale(0.9);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            
            .display {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 15px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                min-height: 80px;
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
                align-items: flex-end;
                word-wrap: break-word;
                word-break: break-all;
            }
            
            .display-operation {
                color: rgba(255, 255, 255, 0.6);
                font-size: 1rem;
                margin-bottom: 0.5rem;
                min-height: 1.2rem;
            }
            
            .display-result {
                color: #ffffff;
                font-size: 2.5rem;
                font-weight: 700;
                min-height: 3rem;
            }
            
            .buttons {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 12px;
            }
            
            button {
                border: none;
                border-radius: 12px;
                font-size: 1.5rem;
                font-weight: 600;
                padding: 1.2rem;
                cursor: pointer;
                transition: all 0.2s ease;
                font-family: 'Inter', sans-serif;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            }
            
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
            }
            
            button:active {
                transform: translateY(0);
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            }
            
            .btn-number {
                background: rgba(255, 255, 255, 0.9);
                color: #333;
            }
            
            .btn-number:hover {
                background: rgba(255, 255, 255, 1);
            }
            
            .btn-operator {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
            }
            
            .btn-operator:hover {
                background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
            }
            
            .btn-clear {
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                color: white;
            }
            
            .btn-clear:hover {
                background: linear-gradient(135deg, #fee140 0%, #fa709a 100%);
            }
            
            .btn-equals {
                background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
                color: white;
                grid-column: span 2;
            }
            
            .btn-equals:hover {
                background: linear-gradient(135deg, #330867 0%, #30cfd0 100%);
            }
            
            .error {
                color: #ff6b6b;
                animation: shake 0.5s ease-in-out;
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-10px); }
                75% { transform: translateX(10px); }
            }
            
            h1 {
                color: white;
                text-align: center;
                margin-bottom: 1.5rem;
                font-size: 2rem;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
        </style>
    </head>
    <body>
        <ul class="circles">
            <li></li><li></li><li></li><li></li><li></li>
            <li></li><li></li><li></li><li></li><li></li>
        </ul>
        
        <div class="calculator">
            <h1>✨ Calculator</h1>
            <div class="display">
                <div class="display-operation" id="operation"></div>
                <div class="display-result" id="result">0</div>
            </div>
            <div class="buttons">
                <button class="btn-clear" onclick="clearDisplay()">C</button>
                <button class="btn-operator" onclick="appendOperator('/')">/</button>
                <button class="btn-operator" onclick="appendOperator('*')">×</button>
                <button class="btn-operator" onclick="deleteChar()">⌫</button>
                
                <button class="btn-number" onclick="appendNumber('7')">7</button>
                <button class="btn-number" onclick="appendNumber('8')">8</button>
                <button class="btn-number" onclick="appendNumber('9')">9</button>
                <button class="btn-operator" onclick="appendOperator('-')">−</button>
                
                <button class="btn-number" onclick="appendNumber('4')">4</button>
                <button class="btn-number" onclick="appendNumber('5')">5</button>
                <button class="btn-number" onclick="appendNumber('6')">6</button>
                <button class="btn-operator" onclick="appendOperator('+')">+</button>
                
                <button class="btn-number" onclick="appendNumber('1')">1</button>
                <button class="btn-number" onclick="appendNumber('2')">2</button>
                <button class="btn-number" onclick="appendNumber('3')">3</button>
                <button class="btn-number" onclick="appendNumber('0')">0</button>
                
                <button class="btn-number" onclick="appendNumber('.')">.</button>
                <button class="btn-equals" onclick="calculate()">=</button>
            </div>
        </div>
        
        <script>
            let currentInput = '0';
            let operation = '';
            let firstOperand = null;
            let waitingForSecondOperand = false;
            
            const resultDisplay = document.getElementById('result');
            const operationDisplay = document.getElementById('operation');
            
            function updateDisplay() {
                resultDisplay.textContent = currentInput;
                resultDisplay.classList.remove('error');
            }
            
            function appendNumber(num) {
                if (waitingForSecondOperand) {
                    currentInput = num;
                    waitingForSecondOperand = false;
                } else {
                    if (currentInput === '0' && num !== '.') {
                        currentInput = num;
                    } else if (num === '.' && currentInput.includes('.')) {
                        return;
                    } else {
                        currentInput += num;
                    }
                }
                updateDisplay();
            }
            
            function appendOperator(op) {
                const inputValue = parseFloat(currentInput);
                
                if (firstOperand === null) {
                    firstOperand = inputValue;
                } else if (operation) {
                    calculate();
                    firstOperand = parseFloat(currentInput);
                }
                
                waitingForSecondOperand = true;
                operation = op;
                operationDisplay.textContent = `${firstOperand} ${getOperatorSymbol(op)}`;
            }
            
            function getOperatorSymbol(op) {
                const symbols = {'+': '+', '-': '−', '*': '×', '/': '÷'};
                return symbols[op] || op;
            }
            
            function getOperationName(op) {
                const names = {'+': 'add', '-': 'subtract', '*': 'multiply', '/': 'divide'};
                return names[op];
            }
            
            async function calculate() {
                if (firstOperand === null || !operation) return;
                
                const secondOperand = parseFloat(currentInput);
                
                try {
                    const response = await fetch('/api/calculate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            operation: getOperationName(operation),
                            num1: firstOperand,
                            num2: secondOperand
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        currentInput = data.error;
                        resultDisplay.classList.add('error');
                    } else {
                        currentInput = String(data.result);
                        operationDisplay.textContent = `${firstOperand} ${getOperatorSymbol(operation)} ${secondOperand} =`;
                    }
                    
                    updateDisplay();
                    firstOperand = null;
                    operation = '';
                    waitingForSecondOperand = true;
                    
                } catch (error) {
                    currentInput = 'Error';
                    resultDisplay.classList.add('error');
                    updateDisplay();
                }
            }
            
            function clearDisplay() {
                currentInput = '0';
                operation = '';
                firstOperand = null;
                waitingForSecondOperand = false;
                operationDisplay.textContent = '';
                updateDisplay();
            }
            
            function deleteChar() {
                if (currentInput.length > 1) {
                    currentInput = currentInput.slice(0, -1);
                } else {
                    currentInput = '0';
                }
                updateDisplay();
            }
            
            // Keyboard support
            document.addEventListener('keydown', (e) => {
                if (e.key >= '0' && e.key <= '9' || e.key === '.') {
                    appendNumber(e.key);
                } else if (e.key === '+' || e.key === '-' || e.key === '*' || e.key === '/') {
                    appendOperator(e.key);
                } else if (e.key === 'Enter' || e.key === '=') {
                    e.preventDefault();
                    calculate();
                } else if (e.key === 'Escape' || e.key === 'c' || e.key === 'C') {
                    clearDisplay();
                } else if (e.key === 'Backspace') {
                    deleteChar();
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        operation = data.get('operation')
        num1 = data.get('num1')
        num2 = data.get('num2')
        
        # Validate inputs
        if operation not in ['add', 'subtract', 'multiply', 'divide']:
            return jsonify({'error': 'Invalid operation'}), 400
        
        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            return jsonify({'error': 'Invalid numbers'}), 400
        
        # Perform calculation
        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                return jsonify({'error': 'Cannot divide by zero'}), 400
            result = num1 / num2
        
        # Round to avoid floating point precision issues
        result = round(result, 10)
        
        return jsonify({'result': result})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
