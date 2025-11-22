from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    """Display the form asking for L or R input"""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handle the form submission"""
    direction = request.form.get('direction', '').upper()
    
    if direction in ['L', 'R']:
        message = f"Selected: {direction}"
        # TODO: Add code here to send direction to Arduino via UDP
        print(f"Direction selected: {direction}")
        return render_template('index.html', message=message)
    else:
        message = "Invalid input. Please select L or R."
        return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
