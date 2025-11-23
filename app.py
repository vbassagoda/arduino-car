from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    """Display the control buttons"""
    return render_template('index.html')

@app.route('/direction', methods=['POST'])
def direction():
    """Handle direction button clicks"""
    data = request.get_json()
    direction = data.get('direction', '').upper()
    
    if direction in ['L', 'R', 'F']:
        print(f"Direction selected: {direction}")
        # TODO: Add code here to send direction to Arduino via UDP
        return jsonify({'success': True, 'message': f"Selected: {direction}"})
    else:
        return jsonify({'success': False, 'message': "Invalid direction"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
