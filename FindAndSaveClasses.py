from pyAudioAnalysis import audioSegmentation as aS
import numpy as np
import time
import os
import multiprocessing
import argparse


queue = multiprocessing.JoinableQueue()

parser = argparse.ArgumentParser()
parser.add_argument("directory", help="set the directory to analyze",
                    type=str)
parser.add_argument("--processes", help="set the amount of processes to use", type=int)
args = parser.parse_args()
sound_files = os.listdir(args.directory)

def set_amount_processes():
    processes = 1
    if multiprocessing.cpu_count() > 1:
        processes = multiprocessing.cpu_count() - 1
    if args.processes:
        processes = args.processes
    return processes

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
            save_out(args.directory + soundfile)
            self.queue.task_done()

start = time.time()
def main():
    processes = set_amount_processes()
    print("Started with " + str(processes))
    for _ in range(processes):
        t = ProcessSound(queue)
        t.daemon = True
        t.start()

    for soundfile in sound_files:
        queue.put(soundfile)

    queue.join()

main()
print "Elapsed Time: %s" % (time.time() - start)
