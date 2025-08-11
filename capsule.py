import os
import json
import sqlite3

def getCapsuleBackend(sqlliteDB=None):
    if sqlliteDB:
        conn = sqlite3.connect(sqlliteDB)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS capsules (
                id TEXT PRIMARY KEY,
                data TEXT
            )
        ''')
        conn.commit()
        conn.close()

        def saveCapsule(capsule):
            conn = sqlite3.connect(sqlliteDB)
            conn.execute(
                'INSERT OR REPLACE INTO capsules (id, data) VALUES (?, ?)',
                (capsule['id'], json.dumps(capsule))
            )
            conn.commit()
            conn.close()

        def loadCapsules():
            conn = sqlite3.connect(sqlliteDB)
            cursor = conn.execute('SELECT data FROM capsules')
            capsules = [json.loads(row[0]) for row in cursor.fetchall()]
            conn.close()
            return capsules

        def findCapsule(capsule_id):
            conn = sqlite3.connect(sqlliteDB)
            cursor = conn.execute('SELECT data FROM capsules WHERE id = ?', (capsule_id,))
            row = cursor.fetchone()
            conn.close()
            return json.loads(row[0]) if row else None
    else:
        def saveCapsule(capsule):
            if os.path.exists('capsules.json'):
                with open('capsules.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = []
            data.append(capsule)
            with open('capsules.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        def loadCapsules():
            if not os.path.exists('capsules.json'):
                return []
            with open('capsules.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        def findCapsule(capsule_id):
            capsules = loadCapsules()
            return next((c for c in capsules if c['id'] == capsule_id), None)
    return saveCapsule, loadCapsules, findCapsule