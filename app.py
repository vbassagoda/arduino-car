from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML template with form for L or R input
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arduino Car Control</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .form-group {
            margin: 20px 0;
        }
        label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
            color: #555;
        }
        .radio-group {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin: 20px 0;
        }
        .radio-option {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        input[type="radio"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 20px;
        }
        button:hover {
            background-color: #45a049;
        }
        .message {
            margin-top: 20px;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Arduino Car Control</h1>
        <form method="POST" action="/submit">
            <div class="form-group">
                <label>Select Direction:</label>
                <div class="radio-group">
                    <div class="radio-option">
                        <input type="radio" id="left" name="direction" value="L" required>
                        <label for="left">L (Left)</label>
                    </div>
                    <div class="radio-option">
                        <input type="radio" id="right" name="direction" value="R" required>
                        <label for="right">R (Right)</label>
                    </div>
                </div>
            </div>
            <button type="submit">Submit</button>
        </form>
        {% if message %}
        <div class="message success">
            {{ message }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Display the form asking for L or R input"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/submit', methods=['POST'])
def submit():
    """Handle the form submission"""
    direction = request.form.get('direction', '').upper()
    
    if direction in ['L', 'R']:
        message = f"Selected: {direction}"
        # TODO: Add code here to send direction to Arduino via UDP
        print(f"Direction selected: {direction}")
        return render_template_string(HTML_TEMPLATE)
    else:
        message = "Invalid input. Please select L or R."
        return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
