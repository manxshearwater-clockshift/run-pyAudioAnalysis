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
    listx = []
    for hour in range(0, 24):
        tuple_list = dh.get_one_hour(bird, day, hour)

        # classe voor shuffling per bird anders
        if bird == "b73":
            amount_shuffles = extract_shuffles(tuple_list, 3)

        else :
            amount_shuffles = extract_shuffles(tuple_list, 2)
        listx.append(amount_shuffles)
    return listx

def running_mean(x, N):
    y = np.zeros((len(x),))
    for ctr in range(len(x)):
         y[ctr] = np.sum(x[ctr:(ctr+N)])
    return y/N

def plot_one_day(listx, day, color):
    pl.plot(list(range(0, len(listx))), listx, color, label="Day " + str(day))

def avlist(list_):
    avlist =[]
    minlength = min(len(x) for x in list_)
    for i in range(minlength):
        elements = [elem[i] for elem in list_]
        avlist.append(sum(elements)/ len(elements))

    return avlist

def plot_average_day(listx, listy):
    listxx = avlist(listx)
    listyy = avlist(listy)

    ax = pl.subplot(111)

    pl.plot(list(range(0, len(listxx))), listxx, "blue", label="unshifted days")
    pl.plot(list(range(0, len(listyy))), listyy,"red", label="shifted days")

    box = ax.get_position()
    ax.set_position([box.x0,box.y0,box.width * 0.8,box.height])
    ax.legend(loc="center left",bbox_to_anchor=(1,0.5))
    pl.show()

def plot_all_days(bird, start_day, stop_day):
    colors = {16: 'r', 17:'g', 18:'b', 19:'y', 20:'magenta', 21:'black', 22: 'r', 23: 'g', 24:'b'}
    ax = pl.subplot(111)
    for day in range(start_day, stop_day + 1):
        no_running_mean_list = one_day_shuffles_per_hour(bird, day)
        running_mean_list = running_mean(no_running_mean_list, 5)
        plot_one_day(running_mean_list, day, colors[day])

    box = ax.get_position()
    ax.set_position([box.x0,box.y0,box.width * 0.8,box.height])
    ax.legend(loc="center left",bbox_to_anchor=(1,0.5))
    pl.show()

def plot_compare(bird):
    total_list =[]
    total_list1 =[]

    for day in range(16, 22):
        no_running_mean_list = one_day_shuffles_per_hour(bird,day)
        running_mean_list = running_mean(no_running_mean_list, 5)
        total_list.append(running_mean_list)

    for day in range(22, 25):
        no_running_mean_list1 = one_day_shuffles_per_hour(bird, day)
        running_mean_list1 = running_mean(no_running_mean_list1, 5)
        total_list1.append(running_mean_list1)

    plot_average_day(total_list,total_list1 )



if __name__ == '__main__':
    dh.drop_db("TABLE_BIRDS")
    dh.create_db()
    dh.csv_to_db("b73.csv", "b73")

    input_bird = raw_input(("Which bird do you want to analyze(b73, b151, b179, DB4, DB20, DB30): \n"))
    input_string = raw_input(("Which graph do you want to plot? for unshifted(typ unshifted), shifted days(typ shifted), to compare shifted and unshifted(typ compare) \n"))

    if input_string == "unshifted":
        plot_all_days(input_bird, 16, 21)

    if input_string == "shifted":
        plot_all_days(input_bird, 22, 24)

    if input_string == "compare":
        plot_compare(input_bird)
