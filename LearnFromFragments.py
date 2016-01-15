from pyAudioAnalysis import audioTrainTest as aT
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("root", help="directory with training examples per bird",
                    type=str)
args = parser.parse_args()

birds = ['Trainings_b151', 'Trainings_b174', 'Trainings_b179', 'Trainings_DB12', 'Trainings_DB20', 'Trainings_DB30', 'Trainings_b73', 'Trainings_DB4']

'''
EG: aT.featureAndTrain(["Fragments/Shuffle/","Fragments/Silence/","Fragments/Micbeep/", "Fragments/Backgroundbird1/"],
    1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "manxknn")
'''
if __name__ == "__main__":
    root = args.root

    for bird in birds:
        bird_birds_dir = os.listdir(root + bird)
        sound_fragmentdir_list = [root + '/' + bird + '/' + sound_dir
                for sound_dir in bird_birds_dir
                if len(os.listdir(root + '/' + bird + '/' + sound_dir)) > 1]
        aT.featureAndTrain(sound_fragmentdir_list, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "knnmodel" + bird)