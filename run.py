import profile

from pyAudioAnalysis import audioTrainTest as aT
from pyAudioAnalysis import audioSegmentation as aS

aT.featureAndTrain(["Fragments/Shuffle/","Fragments/Silence/","Fragments/Micbeep/"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "manxknn")

def run_example(test_file, model_file, segments_file):
	[flagsInd, classesAll, acc] = aS.mtFileClassification(test_file, model_file, "knn", True, segments_file)

run_example("3min_sk_csauth_fast_b73_150616_007_011016.wav", "manxknn", "3min_sk_csauth_fast_b73_150616_007_011016.segments")
run_example("10min_sk_csauth_fast_b73_150621_012_201430.wav", "manxknn", "10min_sk_csauth_fast_b73_150621_012_201430.segments")
