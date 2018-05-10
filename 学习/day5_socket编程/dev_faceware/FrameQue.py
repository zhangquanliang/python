from queue import Queue


threshold = 30


class FrameQue:
    def __init__(self):
        self._que = Queue()
    
    def get(self):
        return self._que.get()
    
    def put(self, data):
        if self._que.qsize() > threshold:
            self.clear()  #如果存储帧数据过多,清空队列维持最新数据
        self._que.put(data)

    def clear(self):
        while not self._que.empty():
            self._que.get_nowait()

    def empty(self):
        return self._que.empty()

