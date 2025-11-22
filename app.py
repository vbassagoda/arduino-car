from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Display the form and handle form submission"""
    message = None
    
    if request.method == 'POST':
        direction = request.form.get('direction', '').upper()
        
        if direction in ['L', 'R', 'F']:
            message = f"Selected: {direction}"
            print(f"Direction selected: {direction}")
            # TODO: Add code here to send direction to Arduino via UDP
        else:
            message = "Invalid input. Please select L, R, or F."
    
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
