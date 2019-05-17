import requests
import json
from flask import Flask, jsonify, request
from time import sleep
import datetime


class deneme():
    def __init__(self):
        processlist = ["Pasting",
                       "Chip_Placing",
                       "Multifunction_Chip_Placing",
                       "Chip_Heating",
                       "Visual_Testing",
                       "Detail_Testing",
                       "Integrated_Chip_Testing",
                       "Socket_Testing",
                       "BIOS_Installing",
                       "Packaging"]
        machinelist = ["Solder_Paste_Printer",
                       "High_Speed_Chip_Placer",
                       "Multifunction_Chip_Placer",
                       "Reflow_Oven_Machine",
                       "Visual_Inspected_Machine",
                       "Automated_Optical_Inspection_Machine",
                       "Integrated_Chip_Test_Machine",
                       "Dual_Inline_Package_Machine",
                       "Digital_Tester_Machine",
                       "Package_Machine"]

        Barcode = 123654852
        PartNo = 25042019
 
        for x in range(0, 100):
            for i in range(0, len(processlist)):
               

                response = {"FactoryName": "MSI-MOTHERBORD-FACTORY",
                            "MachineName": machinelist[i],
                            "ProcessName": processlist[i],
                            "ProcessStartDate": "23.04.2019-16.25.35",
                            "Barcode": Barcode,
                            "ProcessEndDate":"23.04.2019-16.34.35",
                            "PartNo": PartNo,
                            "ProcessIsSuccess": 1}
                self.ProcessSendData(response)
                # sleep(1)
            Barcode = Barcode+1

    def ProcessSendData(self, response):
        datas = json.dumps(response)
        r = requests.post('http://localhost:5000/transactions/new',
                          headers={"Content-Type": "application/json"}, data=datas)
        print(r.status_code)
        # sleep(1)
        r = requests.get('http://localhost:5000/mine')
        print(r.status_code)


deneme()
