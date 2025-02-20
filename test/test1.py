import threading, time
from random import randint


class Producer(threading.Thread):
    def run(self):
        global L
        while True:
            val = randint(0, 100)
            print('生产者', self.name, ":Append" + str(val), L)
            if lock_con.acquire():
                L.append(val)
                lock_con.notify()  # 通知消费者可以吃包子了，激活wait。
                lock_con.release()
            time.sleep(3)


class Consumer(threading.Thread):
    def run(self):
        global L
        while True:
            lock_con.acquire()  # wait阻塞后，从这里开始这行，重新获得锁。
            if len(L) == 0:  # 如果包子架或容器中没有包子，则等待。
                lock_con.wait()  # wait的作用：1、释放锁；2、阻塞，等待notify通知
            print('消费者', self.name, ":Delete" + str(L[0]), L)
            del L[0]
            lock_con.release()
            time.sleep(1)


if __name__ == "__main__":
    L = []  # 装包子的架子或容器
    lock_con = threading.Condition()  # 创建一把条件同步变量的锁。
    threads = []
    for i in range(5):
        threads.append(Producer())
    threads.append(Consumer())
    for t in threads:
        t.start()  # start了6个线程对象。
    for t in threads:
        t.join()
    print('-------xiaohuchengsi,haha----------')