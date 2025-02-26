import threading
import time
from queue import Queue

shared_data = None
sync_queue = Queue(maxsize=1)
try:
    # print(sync_queue.get(block=False))
    pass
except Exception as e:
    # print("hello", flush=True)
    pass



# def writer():
#     global shared_data
#     write_list = []
#     for i in range(1,  5):
#         # 注意一定要先放入
#         sync_queue.put("")
#         shared_data = i
#         write_list.append(shared_data)
#     print(f"write list: {write_list}")
#
#
# def reader():
#     global shared_data
#     read_list = []
#     for i in range(1,  5):
#         sync_queue.get()
#         read_list.append(shared_data)
#     print(f"\nread list: {read_list}")
#
#
# # 创建并启动线程
# writer_thread = threading.Thread(target=writer)
# reader_thread = threading.Thread(target=reader)
# writer_thread.start()
# reader_thread.start()
# writer_thread.join()  # 等待写线程完成（实际应用中可能需要更复杂的同步机制）
# reader_thread.join()  # 等待读线程完成（实际应用中可能需要更复杂的同步机制）
