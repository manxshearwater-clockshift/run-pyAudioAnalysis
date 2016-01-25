import DatabaseHelper as dh
import matplotlib.pyplot as pl
import numpy as np


def extract_shuffles(tuple_list, class_nr):
    count = 0
    for tuple in tuple_list:
        if class_nr == tuple[0]:
            count += 1
    return count


def one_day_shuffles_per_hour(bird, day):
    listx = 24 * [0]
    for hour in range(0, 24):
        tuple_list = dh.get_one_hour(bird, day, hour)
        total_events = len(tuple_list)
        if total_events == 0:
            print "No events at ", (day, hour)
            continue
        # classe voor shuffling per bird anders
        if bird == "b73":
            shuffle_class = 0
        elif bird == "DB4":
            shuffle_class = 1
        else:
            shuffle_class = 3
        amount_shuffles = extract_shuffles(tuple_list, shuffle_class)
        normalized_shuffles = (float(amount_shuffles) / float(total_events)) * 3600
        listx[hour] = normalized_shuffles

    return listx


def running_mean(x, N):
    meanList = np.zeros(len(x))
    for y in range(len(x)):
        tempList = np.zeros((N*2)+1)
        tempList[N] = x[y]
        for z in range(1, N+1):
            if(y-z)<0:
                p = len(x)-np.abs(y-z)
            else:
                p = y-z
            if(y+z)>=len(x):
                q = y+z-len(x)
            else:
                q = y+z
            tempList[N-z] = x[p]
            tempList[N+z] = x[q]
        meanList[y] = np.mean(tempList)
    return meanList


def plot_one_day(listx, day, color):
    pl.plot(list(range(0, len(listx))), listx, color, label="Day " + str(day))


def avlist(list_):
    avlist =[]
    minlength = min(len(x) for x in list_)
    for i in range(minlength):
        elements = [elem[i] for elem in list_]
        avlist.append(sum(elements)/ len(elements))

    return avlist


def minlist(list_):
    minslist =[]
    minlength = min(len(x) for x in list_)
    for i in range(minlength):
        elements = [elem[i] for elem in list_]
        minslist.append(min(elements))
    return minslist


def maxlistf(list_):
    maxslist =[]
    minlength = min(len(x) for x in list_)
    for i in range(minlength):
        elements = [elem[i] for elem in list_]
        maxslist.append(max(elements))
    return maxslist


def plot_average_day(listx, listy, bird):
    listxx = avlist(listx)
    listyy = avlist(listy)

    listyy = normalize_running_means(listyy, listxx)

    ax = pl.subplot(111)

    pl.plot(list(range(0, len(listxx))), listxx, "blue", label="unshifted days")
    pl.plot(list(range(0, len(listyy))), listyy,"red", label="shifted days")

    box = ax.get_position()
    ax.set_position([box.x0,box.y0,box.width * 0.8,box.height])
    ax.legend(loc="center left",bbox_to_anchor=(1,0.5))
    pl.xlabel("hours")
    pl.ylabel("amount of shuffles")
    pl.title(bird)
    pl.show()

def plot_all_days(bird, start_day, stop_day):
    colors = {16: 'r', 17:'g', 18:'b', 19:'y', 20:'magenta', 21:'black', 22: 'r', 23: 'g', 24:'b'}
    ax = pl.subplot(111)
    for day in range(start_day, stop_day + 1):
        no_running_mean_list = one_day_shuffles_per_hour(bird, day)
        running_mean_list = running_mean(no_running_mean_list, 2)
        plot_one_day(running_mean_list, day, colors[day])

    box = ax.get_position()
    ax.set_position([box.x0,box.y0,box.width * 0.8,box.height])
    ax.legend(loc="center left",bbox_to_anchor=(1,0.5))
    pl.xlabel("hours")
    pl.ylabel("amount of shuffles")
    pl.title(bird)
    pl.show()


def plot_compare(bird):
    total_list =[]
    total_list1 =[]

    for day in range(16, 22):
        no_running_mean_list = one_day_shuffles_per_hour(bird,day)
        running_mean_list = running_mean(no_running_mean_list, 2)
        total_list.append(running_mean_list)

    for day in range(22, 25):
        no_running_mean_list1 = one_day_shuffles_per_hour(bird, day)
        running_mean_list1 = running_mean(no_running_mean_list1, 2)
        total_list1.append(running_mean_list1)

    plot_average_day(total_list,total_list1, bird )


def compare_seperateshifted(bird):
    total_list =[]
    for day in range(16, 22):
        no_running_mean_list = one_day_shuffles_per_hour(bird, day)
        running_mean_list = running_mean(no_running_mean_list, 2)
        total_list.append(running_mean_list)
    avlists = avlist(total_list)
    pl.plot(list(range(0, len(avlists))), avlists, "blue", label="unshifted days")

    colors = {22: 'r', 23: 'g', 24:'black'}
    for day in range(22, 25):
        no_running_mean_list = one_day_shuffles_per_hour(bird, day)
        running_mean_list = running_mean(no_running_mean_list, 2)
        plot_one_day(running_mean_list, day, colors[day])

    ax = pl.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0,box.y0,box.width * 0.8, box.height])
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    pl.xlabel("hours")
    pl.ylabel("amount of shuffles")
    pl.title(bird)

    pl.show()


def compare_nonshifted_minmax(bird):
    total_list = []
    for day in range(16, 22):
        no_running_mean_list = one_day_shuffles_per_hour(bird, day)
        running_mean_list = running_mean(no_running_mean_list, 2)
        total_list.append(running_mean_list)
    avlists = avlist(total_list)
    pl.plot(list(range(0, len(avlists))), avlists, "black", label="unshifted days")

    minslist = minlist(total_list)
    pl.plot(list(range(0, len(minslist))), minslist, "blue", label="min")

    maxlist = maxlistf(total_list)
    pl.plot(list(range(0, len(maxlist))), maxlist, "red", label="max")

    colors = {22: 'orange', 23: 'grey', 24: 'darkmagenta'}
    for day in range(22, 25):
        no_running_mean_list = one_day_shuffles_per_hour(bird, day)
        running_mean_list = running_mean(no_running_mean_list, 2)
        plot_one_day(running_mean_list, day, colors[day])

    ax = pl.subplot(111)
    pl.fill_between(list(range(0, len(maxlist))), minslist, maxlist, facecolor='lightgreen', alpha=0.5)
    box = ax.get_position()
    ax.set_position([box.x0,box.y0,box.width * 0.8, box.height])
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    pl.xlabel("hours")
    pl.ylabel("amount of shuffles")
    pl.title(bird)

    pl.show()


def normalize_running_means(shifted_list, unshifted_list):
    standard = sum(unshifted_list)
    total_in_shifted_list = sum(shifted_list)
    for i in range(0, len(shifted_list)):
        print(shifted_list[i])
        shifted_list[i] = (shifted_list[i] * standard) / total_in_shifted_list
        print(shifted_list[i])
    return shifted_list



if __name__ == '__main__':
    input_bird = raw_input(("Which bird do you want to analyze(b73, b174, b179, DB4, DB20, DB30): \n"))
    input_string = raw_input(("Which graph do you want to plot? for unshifted(typ unshifted), shifted days(typ shifted), to compare shifted and unshifted(typ compare) \n"))

    if input_string == "unshifted":
        plot_all_days(input_bird, 16, 21)

    if input_string == "shifted":
        plot_all_days(input_bird, 22, 24)

    if input_string == "compare":
        plot_compare(input_bird)

    if input_string == "compare_seperateshifted":
        compare_seperateshifted(input_bird)

    if input_string == "compare_nonshifted_minmax":
        compare_nonshifted_minmax(input_bird)

    print("Shifts: b73-FAST, b174-FAST, b179-SOFT, DB4-FAST, DB20-FAST, DB30-SLOW")

