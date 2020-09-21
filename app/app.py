from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# CORS(app)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # if request.method == 'POST':
    #     uploaded_file = request.files['file']
    #     if uploaded_file.filename != '':
    #         image = uploaded_file
    #         payload = {"image": image}
    #         # url = 'http://localhost:5000/predict'
    #         r = requests.post(api_endpoint, files=payload).json()
    #         res = make_response(jsonify(r), 200)
    #         return res

    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)  