from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/create')
def create():
    return render_template('create.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)