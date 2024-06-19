from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        result = subprocess.run(['python3', 'code.py'], capture_output=True, text=True)
        return jsonify({"output": result.stdout, "error": result.stderr})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
