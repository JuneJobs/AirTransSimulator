import threading, random, time, http.client
# discription Simualtor
# author      Junhee Park (j.jobs1028@gmail.com)
# since       2018. 10. 26.
# last update 2018. 10. 26.

class Simulator:
    def __init__(self):
        self.id = 0
        self.transferInterval = 30  #sec
        self.measureInterval = 1    #sec
        self.measuredDataSet = []
        self.transferringDataSet = {}
        self.response = {}
    
    def storeMeasuredData(self, timestamp, data):
        self.measuredDataSet.append(data)

    def getMeasuredDataSet(self):
        return self.measuredDataSet

    def clearMeasuredDataSet(self):
        self.measuredDataSet = []

    def setTransferringDataSet(self, dataset):
        self.transferringDataSet = dataset

    def getTimeStamp(self):
        return int(time.time())

    def getTempData(self):
        return random.randint(20, 30)

    def getRawData(self):
        return round(random.uniform(1, 99), 2)

    def getAqiData(self):
        return random.randint(1, 500)

    def bulidCsv(self, target, string):
        return target + ',' + str(string) if target != '' else str(string)

    def encodeData(self, target, data):
        target.append(data)

    def animator(self, cnt):
        strSquare = ''
        for i in range(1, cnt + 1):
            strSquare += '■'
        for i in range(1, self.transferInterval - cnt):
            strSquare += '□'
        strSquare += ' '+ str(int(cnt/self.transferInterval*100)) + '%'
        return strSquare

    def connection(self, message):
        conn = http.client.HTTPConnection("localhost:8080/serverapi")
        body = message
        headers = {
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
        }
        conn.request("POST", "serverapi", body, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    def msgPacking(self):
        return {
            "header": {
                "msgType": 4,
                "msgLen": self.transferInterval,
                "endpointId": 1
            },
            "payload": {
                self.measuredDataSet
            }
        }

    def measureData(self):
        print('Measuring ' + self.animator(len(self.measuredDataSet)))
        timestamp = self.getTimeStamp()
        measuredData = []
        self.encodeData(measuredData, timestamp)
        self.encodeData(measuredData, self.getTempData())
        self.encodeData(measuredData, timestamp)  # Timestamp
        self.encodeData(measuredData, self.getTempData())  # Temperature
        self.encodeData(measuredData, self.getRawData())   # CO
        self.encodeData(measuredData, self.getRawData())   # O3
        self.encodeData(measuredData, self.getRawData())   # NO2
        self.encodeData(measuredData, self.getRawData())   # SO2
        self.encodeData(measuredData, self.getRawData())   # PM2.5
        self.encodeData(measuredData, self.getRawData())   # PM10
        self.encodeData(measuredData, self.getAqiData())   # CO AQI
        self.encodeData(measuredData, self.getAqiData())   # O3 AQI
        self.encodeData(measuredData, self.getAqiData())   # NO2 AQI
        self.encodeData(measuredData, self.getAqiData())   # SO2 AQI
        self.encodeData(measuredData, self.getAqiData())   # PM2.5 AQI
        self.encodeData(measuredData, self.getAqiData())   # PM10 AQI
        self.storeMeasuredData(timestamp, measuredData)
        print('Response >>\n' + str(self.response))
        threading.Timer(self.measureInterval, self.measureData).start()


    def transferData(self):
        measuredDataSet = self.getMeasuredDataSet()
        if len(measuredDataSet) > 1:
            self.clearMeasuredDataSet()
            self.setTransferringDataSet(measuredDataSet)
            print('Transfer >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n', self.msgPacking())
        threading.Timer(self.transferInterval, self.transferData).start()

    def run(self):
        self.measureData()
        self.transferData()





def main():
    app = Simulator()
    app.run()

if __name__ == '__main__':
    main()
