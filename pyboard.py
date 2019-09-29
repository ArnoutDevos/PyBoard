import requests
import os
import threading
import time

class PyBoard:
    def __init__(self, ylabel="Loss", xlabel="Epoch", max_points=10):
        self.data = []
        self.max_points = max_points
        self.xlabel = xlabel
        self.ylabel = ylabel

    def start(self):
        myCmd = 'pkill -9 python'
        os.system(myCmd)
        myCmd = 'python ./main.py &'
        os.system(myCmd)
        time.sleep(2)

    def log(self, data):
        self.data.append(data)

        ys = [d['y'] for d in self.data]
        xs = [d['x'] for d in self.data]

        r = requests.post('http://localhost:5000/send',
						json={'values':ys[::max([1,int(len(ys)/10)])],
						'labels':xs[::max([1,int(len(ys)/self.max_points)])]})