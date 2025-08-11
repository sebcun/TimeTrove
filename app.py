import os
import json
import uuid
import pytz
import logging
from datetime import datetime
from time import time
from flask import (
    Flask, render_template, request, redirect, jsonify,
    send_from_directory, current_app
)
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from capsule import getCapsuleBackend

# Load environment variables from .env file
load_dotenv()

def startTimeTrove():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['UPLOAD_FOLDER'] = 'static/uploads'

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
    )

    saveCapsule, loadCapsules, findCapsule = getCapsuleBackend(
        sqlite_db=os.getenv('SQLITE_DB')
    )

    @app.route('/')
    def home():
        """Render the home page."""
        return render_template('index.html')

    @app.route('/faq')
    def faq():
        """Render the FAQ page."""
        return render_template('faq.html')

    @app.route('/create', methods=['GET', 'POST'])
    def create():
        """Create a new time capsule."""
        if request.method == 'POST':
            try:
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
                            originalFileName = secure_filename(file.filename)
                            uniqueId = str(uuid.uuid4())
                            ext = os.path.splitext(originalFileName)[1]
                            uniqueFileName = f"{uniqueId}{ext}"
                            savePath = os.path.join(current_app.config['UPLOAD_FOLDER'], uniqueFileName)
                            file.save(savePath)
                            content['serverPath'] = uniqueFileName
                            content['value'] = originalFileName

                capsule = {
                    "id": capsuleID,
                    "name": capsuleName,
                    "description": capsuleDescription,
                    "readyAt": unixReadyAt,
                    "createdAt": int(time()),
                    "contents": capsuleContents
                }

                saveCapsule(capsule)

                logging.info(f"Capsule {capsuleID} created successfully.")
                return jsonify({"success": True, "capsuleID": capsuleID}), 200
            except Exception as e:
                logging.error(f"Error creating capsule: {e}")
                return jsonify({"success": False, "error": str(e)}), 500
        else:
            return render_template('create.html')

    @app.route('/capsule/<capsuleID>')
    def viewCapsule(capsuleID):
        """View a specific time capsule."""
        capsule = findCapsule(capsuleID)
        if not capsule:
            return render_template('capsule/base.html', NOTFOUND=True)
        
        isReady = capsule['readyAt'] <= int(time())
        if isReady:
            return render_template(
                'capsule/base.html',
                NOTFOUND=False,
                READY=True,
                CAPSULEID=capsule['id'],
                CAPSULENAME=capsule['name'],
                CAPSULEDESCRIPTION=capsule['description'],
                CAPSULECONTENTS=capsule['contents'],
                READYAT=capsule['readyAt'],
                CREATEDAT=capsule['createdAt']
            )
        else:
            return render_template(
                'capsule/base.html',
                NOTFOUND=False,
                READY=False,
                READYAT=capsule['readyAt']
            )

    @app.route('/download/<capsuleID>/<filePath>')
    def download(capsuleID, filePath):
        """Download a file from a capsule."""
        capsule = findCapsule(capsuleID)
        if not capsule:
            return render_template('capsule/base.html', NOTFOUND=True)

        content = next((ct for ct in capsule['contents'] if ct.get('serverPath') == filePath), None)
        if not content:
            return "File not found", 404

        originalFileName = content.get('value', filePath)
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filePath,
            as_attachment=True,
            download_name=originalFileName
        )

    return app

if __name__ == '__main__':
    app = startTimeTrove()
    app.run(
        host=os.getenv('FLASK_RUN_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_RUN_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'True').lower() in ['true', '1', 'yes']
    )