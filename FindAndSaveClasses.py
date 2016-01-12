from pyAudioAnalysis import audioSegmentation as aS
import numpy as np
import time
import os
import multiprocessing

root = "/home/yorick/ManxShearwaterProject/TESTpyAudioAnalysis/dir/"
sound_files = os.listdir(root)
queue = multiprocessing.JoinableQueue()

def save_out(test_file):
    [flags_ind, classes_all, acc] = aS.mtFileClassification(test_file, "manxknn", "knn", False)
    np.save(test_file, flags_ind)
    return classes_all

class ProcessSound(multiprocessing.Process):
  def __init__(self, queue):
    multiprocessing.Process.__init__(self)
    self.queue = queue

  def run(self):
    while True:
      soundfile = self.queue.get()
      save_out(root + soundfile)
      self.queue.task_done()

start = time.time()
def main():
  for _ in range(5):
    t = ProcessSound(queue)
    t.daemon(True)
    t.start()

  for soundfile in sound_files:
    queue.put(soundfile)

  queue.join()

main()
print "Elapsed Time: %s" % (time.time() - start)
