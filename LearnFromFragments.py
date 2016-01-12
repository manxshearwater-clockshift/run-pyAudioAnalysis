from pyAudioAnalysis import audioTrainTest as aT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("directories", help="directories as list",
                    type=str)
parser.add_argument("--name", help="the name of the knn model",
                    type=str)
args = parser.parse_args()

modelname = "model"
if args.name:
    modelname = args.name


'''
EG: aT.featureAndTrain(["Fragments/Shuffle/","Fragments/Silence/","Fragments/Micbeep/", "Fragments/Backgroundbird1/"],
    1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "manxknn")

'''

aT.featureAndTrain(args.directories, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", modelname)
