#!/usr/bin/env python
import DatabaseHelper as dh
import numpy as np
import scipy as sp
from scipy import stats


##############################################
# Berekent voor elk uur of de shifted day in het confidence interval zit met gebruik van statistiek.
# Als dit het geval is krijgt deze een score 1, anders score 0
# Dan is de totale score het aantal enen delen door de lengte van de aantal uren(24 dus)
# Het programma shift de shifted list 1 uur per keer en doet dit dus 4 keer
##############################################

# shift list by n steps
# sort_shift can be either slow or fast
def shift_list(list_, n, sort_shift):
    
    # if fast biological clock back
    if sort_shift == "fast":
        shifted_list = np.roll(list_, -n)
    
    # if slow biological clock forward
    elif sort_shift == "slow":
        shifted_list = np.roll(list_,n)
    
    else: 
        print "something went wrong"
    
    return shifted_list

# compute confidence interval given a list
def confidence_interval(list_, confidence_percentage):
    # init parameters
    a_list = 1.0 * np.array(list_)
    n = len(a_list)
    mean = np.mean(a_list)
    std_error = sp.stats.sem(a_list)
    
    # compute interval
    range_interval = std_error *sp.stats.t.ppf((1+confidence_percentage)/2., n-1)
    
    min_i = mean - range_interval
    max_i = mean + range_interval
    return min_i, max_i
    
# check if datapoint is in confidence interval, returns 1 if yes, 0 if no
def check_in_confidence_interval(datapoint, list_, confidence_percentage):
    min_i, max_i = confidence_interval(list_, confidence_percentage)

    # datapoint in interval
    if (datapoint >= min_i) and (datapoint <= max_i):
        score  = 1
        
    else:
        score  = 0
        
    return score
        
# compute percentage of the amount of times where datapoint falls into conf_interval
def score_percentage(list_):
    score = 0
    i = 0
    n = len(list_)
    for i in range(i, len(list_)):
        if list_[i] == 1:
            score += 1
    
    percentage = ((float(score)/ float(n)) * 100)
    
    return percentage
    
# copied from plotscript
def extract_shuffles(tuple_list, class_nr):
    count = 0
    for tuple in tuple_list:
        if class_nr == tuple[0]:
            count += 1
    return count
    
# copied from plotscript
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
        listx[hour] = (normalized_shuffles)
    return listx
    
# make list of all six normal days per hour
# list = [[uur0_day1, uur0_day2,....etc., uur0_day6], [uur1_day1, uur1_day2,....etc., uur1_day6], ...etc tot 24 uur ]
def get_lists_perhour_unshifted_days(bird):

    total_shuffles_x_hours = []
    
    for day in range(16,22):
        shuffles_day = one_day_shuffles_per_hour(bird, day)
        # running_mean_shuffles = running_mean(shuffles_day, 2)
        total_shuffles_x_hours.append(shuffles_day)
        
        
    # transponant is nodig omdat lijst nodig voor per uur voor alle zes dagen 
    x = np.array(total_shuffles_x_hours)
    total_shuffles_x_days = x.T
    return total_shuffles_x_days

# make list for shifted days with x is hours
# list = [[uur0,uur1,...,uur24], [etc..] ]
def get_lists_perhour_shifted_days(bird):

    total_shuffles_x_hours = []
    
    for day in range(22,25):
        shuffles_day = one_day_shuffles_per_hour(bird, day)
        # running_mean_shuffles = running_mean(shuffles_day, 2)
        total_shuffles_x_hours.append(shuffles_day)
        
    return total_shuffles_x_hours
        
# checks what sort of shift belongs to the bird
def slow_or_fast(bird):
    
    if bird == "b73": 
        sort_shift = "fast"
        
    elif bird == "b174":
        sort_shift = "fast"
        
    elif bird == "DB4":
        sort_shift = "fast"
        
    elif bird == "DB20":
        sort_shift = "fast"
        
    elif bird == "b179":
        sort_shift = "slow"
    
    elif bird == "DB30":
        sort_shift = "slow"
    
    else:
        print "Bird does not exist"
        
    return sort_shift
    
def main():
    # get input
    bird = raw_input(("Which bird do you want to test(b73,b174,b179,DB4,DB20,DB30): \n"))
    
    
    # parameters/variables
    sort_shift = slow_or_fast(bird)
    max_shift = 4
    confidence = 0.95
    i = 0
    j = 0
    scorelist = []
    
    # total lijst van de 24 uren van de unshifted dagen 
    unshifted_total = get_lists_perhour_unshifted_days(bird)
    
    # shifted dagen probeer elk drie dagen apart
    shifted_total = get_lists_perhour_shifted_days(bird)
    
    # loop door alle drie shifted days
    shifted_day = 0
    for shifted_day in range(shifted_day, 3):
        
        print "Test for shifted day nr: ", shifted_day + 1
        print ""
        
        shifted_x = shifted_total[shifted_day]
        i = 0
        # check shift per uur per dag (jetlag)
        for i in range(i, max_shift+1):
                scorelist = []
                j=0
                print "After ", i, "hour shift:"
                
                # shift list, per keer 1 uur laten shiften tot max 4 uur
                shifted_xx = shift_list(shifted_x, i, sort_shift)
                
                # berekent score voor alle uren
                for j in range(j, len(shifted_x)):
                    score = check_in_confidence_interval(shifted_xx[j], unshifted_total[j], confidence)
                    scorelist.append(score)
                    # print shifted_xx
                    # print "score: ", score
                    # print ""
                
                # percentage van de totale uren waarin het datapunt in het confidence interval zit
                print "With a confidence of ", confidence , ","
                print score_percentage(scorelist), "% of the hours of the shifted-days falls into a confidence-interval of the unshifted days. "  
                print ""
            
        print("************************************************")
    
if __name__ == '__main__' :
    main()
