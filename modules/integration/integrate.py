import threading
import time
from queue import Queue
import numpy as np


def classify(done, preds, model):
  while not done() or not trial_queue.empty():
    if not trial_queue.empty():
        trial = trial_queue.get()
        probs = model.predict(trial)
        # print(f"classified {probs.argmax()}")
        preds.append(probs.argmax())
        # socket.sendall(bytes([probs.argmax()]))
      


trial_queue = Queue()

def stream(model, test):
    print("starting stream")
    done = False
    preds = []

    x = threading.Thread(target=classify, args=(lambda: done, preds, model))
    x.start()

    for trial in test:
        try:
            trial = np.array([trial])
            # print(trial.shape, trial)
            trial_queue.put(trial)
            time.sleep(0.004)
        except KeyboardInterrupt:
            print("cancel thread")
            break

    done = True
    x.join()

    return preds
