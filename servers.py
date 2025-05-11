import ser
import threading,json
for i in range(1145,1145+int(json.load(open('config.json'))['num'])):
    a = ser.ser(i)
    threading.Thread(target=a.main()).start()
