import cv2
import requests
import sqlite3

connection = sqlite3.connect('parking.db')
cursor = connection.cursor()

vs = cv2.VideoCapture(0)
while True:
    ret,  img = vs.read()
    if not ret:
        print("camera not recognised")
        break
    cv2.imshow('srtream', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('frame.png', img)
        break
vs.release()
cv2.destroyAllWindows()

try:
    with open('frame.png', 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            files=dict(upload=fp),
            headers={'Authorization': 'Token 81dda232b51e3f7c7620f0830834a6d8c94e0120'})
    results = response.json()
    number = results['results'][0]['plate'].upper()
    print(number)

    cursor.execute("select * from history where numberplate = '"+number+"' and entry is null")
    result = cursor.fetchone()
    print(result)
    if result:
        from datetime import datetime
        now = datetime.now()
        Time = now.strftime("%H:%M")
        print("Entry Time:", Time)
        cursor.execute("update history set entry = '"+Time+"' where numberplate = '"+number+"'")
        connection.commit()

        slot = result[5]
        print('slot ', slot)
        f = open('slot.txt', 'w')
        f.write(slot)   
        f.close()
    else:
        print('invalid numberplate')
        f = open('slot.txt', 'w')
        f.write('I')   
        f.close()
except Exception as e:
    print(e)
    print('numberplate not recognised')