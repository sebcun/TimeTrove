from flask import Flask, render_template, request, redirect, jsonify
import os, json, uuid, pytz
from werkzeug.utils import secure_filename
from datetime import datetime
from time import time

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CAPSULES_JSON = 'capsules.json'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        capsuleID = str(uuid.uuid4())
        capsuleName = request.form.get('capsuleName')
        capsuleDescription = request.form.get('capsuleDescription')
        capsuleTime = request.form.get('capsuleTime')
        capsuleDate = request.form.get('capsuleDate')
        userTimeZone = request.form.get('userTimeZone')
        capsuleContents = json.loads(request.form.get('capsuleContents'))

        # Get UNIX timestamp
        dtStr = f"{capsuleDate} {capsuleTime}"
        local = pytz.timezone(userTimeZone)
        dt = local.localize(datetime.strptime(dtStr, "%Y-%m-%d %H:%M"))
        unixReadyAt = int(dt.timestamp())

        for idx, content in enumerate(capsuleContents):
            if content['type'] in ['image', 'file']:
                fileKey = f"{content['type']}_{idx}"
                file = request.files.get(fileKey)
                if file:
                    filename = secure_filename(file.filename)
                    savePath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(savePath)
                    content['value'] = savePath
        capsule = {
            "id": capsuleID,
            "name": capsuleName,
            "description": capsuleDescription,
            "readyAt": unixReadyAt,
            "contents": capsuleContents        
        }

        if os.path.exists(CAPSULES_JSON):
            with open(CAPSULES_JSON, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []
        data.append(capsule)
        with open(CAPSULES_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return jsonify({"success": True, "capsuleID": capsuleID}), 200
    else:
        return render_template('create.html')

@app.route('/capsule/<capsuleID>')
def viewCapsule(capsuleID):
    if not os.path.exists(CAPSULES_JSON):
        return "Capsule not found", 404
    with open (CAPSULES_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find Capsule
    capsule = next((c for c in data if c['id']==capsuleID), None)
    if not capsule:
        return "Capsule not found", 404
    
    isReady = capsule['readyAt'] <= int(time())
    if isReady:
        return capsuleID
    else:
        return str(capsule['readyAt'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)