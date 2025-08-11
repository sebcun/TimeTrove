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
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                capsule_id TEXT,
                email TEXT,
                readyAt INTEGER
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
        
        def registerNotificationEmail(capsuleID, email, readyAt):
            conn = sqlite3.connect(sqlliteDB)
            conn.execute(
                'INSERT INTO notifications (capsule_id, email, readyAt) VALUES (?, ?, ?)',
                (capsuleID, email, readyAt)
            )
            conn.commit()
            conn.close()

        def getAllNotifications():
            conn = sqlite3.connect(sqlliteDB)
            cursor = conn.execute(
                'SELECT id, capsule_id, email, readyAt FROM notifications'
            )
            notifications = [
                {'id': row[0], 'capsuleID': row[1], 'email': row[2], 'readyAt': row[3]}
                for row in cursor.fetchall()
            ]
            conn.close()
            return notifications

        def deleteNotification(notificationID):
            conn = sqlite3.connect(sqlliteDB)
            conn.execute('DELETE FROM notifications WHERE id = ?', (notificationID,))
            conn.commit()
            conn.close()        
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
        def registerNotificationEmail(capsule_id, email, readyAt):
            notificationFile = 'notifications.json'
            if os.path.exists(notificationFile):
                with open(notificationFile, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = []
            if not any(n['capsule_id'] == capsule_id and n['email'] == email for n in data):
                data.append({'capsule_id': capsule_id, 'email': email, 'readyAt': readyAt})
            with open(notificationFile, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        def getAllNotifications():
            notificationFile = 'notifications.json'
            if not os.path.exists(notificationFile):
                return []
            with open(notificationFile, 'r', encoding='utf-8') as f:
                return json.load(f)
        def deleteNotification(notificationID):
            notificationFile = 'notifications.json'
            if not os.path.exists(notificationFile):
                return
            with open(notificationFile, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if 0 <= notificationID < len(data):
                data.pop(notificationID)
                with open(notificationFile, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

    return (
        saveCapsule,
        loadCapsules,
        findCapsule,
        registerNotificationEmail,
        getAllNotifications,
        deleteNotification
    )