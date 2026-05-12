
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

    cursor.execute("select * from history where numberplate = '"+number+"' and exit is null")
    result1 = cursor.fetchone()
    print(result1)
    if result1:
        cursor.execute("select * from wallet where phone = '"+result1[2]+"'")
        result = cursor.fetchone()

        if result:
            Balance = int(result[0])
            if Balance < 100:
                print('insufficient balance')
                f = open('slot.txt', 'w')
                f.write('E')   
                f.close()
            else:
                Entrytime = result1[7]  # example: "13:45"
                from datetime import datetime
                now = datetime.now()
                Time = now.strftime("%H:%M")
                print("Exit Time:", Time)

                # Convert both times to datetime objects
                fmt = "%H:%M"
                entry_dt = datetime.strptime(Entrytime, fmt)
                exit_dt = datetime.strptime(Time, fmt)

                # Compute difference in minutes
                diff_minutes = (exit_dt - entry_dt).total_seconds() / 60

                print("Time difference in minutes:", diff_minutes)

                av_balance = Balance - int(int(diff_minutes) * 10)
                cursor.execute("update wallet set balance = '"+str(av_balance)+"' where phone = '"+result1[2]+"'")
                connection.commit()
                print('amount deducted')
                
                cursor.execute("update history set exit = '"+Time+"', amount = '"+str(50 + int(int(diff_minutes) * 10))+"', status = 'completed' where numberplate = '"+number+"'")
                connection.commit()
                slt = result1[5]
                f = open('slot.txt', 'w')
                f.write(slt)   
                f.close()
        else:
            print('insufficient balance')
            f = open('slot.txt', 'w')
            f.write('E')   
            f.close()
    else:
        print('invalid numberplate')
except Exception as e:
    print(e)
    print('numberplate not recognised')