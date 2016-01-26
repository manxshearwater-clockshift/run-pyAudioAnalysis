import lsanomaly
import DatabaseHelper as dh
import numpy as np
import scipy as sp
from scipy import stats

# predict for every index whether it is anomalous
# returns 'anomaly' if outlier or 0.0 if inlier
def anomaly_list(X_train, X_test):
	# get anomamly prediction
	anomalymodel = lsanomaly.LSAnomaly()
	anomalymodel.fit(X_train)
	anomaly_list = anomalymodel.predict(X_test)
	print anomaly_list
	return anomaly_list

# make list of all six normal days per hour
# list = [[uur0_day1, uur0_day2,....etc., uur0_day6], [uur1_day1, uur1_day2,....etc., uur1_day6], ...etc tot 24 uur ]
def get_lists_perhour_unshifted_days(bird):

	total_shuffles_x_hours = []
	
	for day in range(16,22):
		shuffles_day = one_day_shuffles_per_hour(bird, day)
		# running_mean_shuffles = running_mean(shuffles_day, 2)
		total_shuffles_x_hours.append(shuffles_day)
		
	return total_shuffles_x_hours
	
	
# make list for shifted days with x is hours
# list = [[uur0,uur1,...,uur24], [etc..] ]
def get_lists_perhour_shifted_days(bird):

	total_shuffles_x_hours = []
	
	for day in range(22,25):
		shuffles_day = one_day_shuffles_per_hour(bird, day)
		# running_mean_shuffles = running_mean(shuffles_day, 2)
		total_shuffles_x_hours.append(shuffles_day)
		
	
	return total_shuffles_x_hours
	
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
    
# shift list by n steps
# sort_shift can be either slow or fast
def shift_list(list_, n, sort_shift):
	
	# if fast biological clock back
	if sort_shift == "fast":
		shifted_list = np.roll(list_, n)
	
	# if slow biological clock forward
	elif sort_shift == "slow":
		shifted_list = np.roll(list_,-n)
	
	else: 
		print "something went wrong"
	
	return shifted_list
	
# shift all lists
def shift_all_lists(lists, n, sort_shift):
	i = 0
	length = len(lists)
	total_list = []
	
	for i in range(i, length):
		shifted_list = shift_list(lists[i], n , sort_shift)
		total_list.append(shifted_list)
	
	return total_list
		
		
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
	
	# databast input
	bird = raw_input(("Which bird do you want to test(b73,b174,b179,DB4,DB20,DB30): \n"))
	X_train = np.array(get_lists_perhour_unshifted_days(bird))
	X_test = np.array(get_lists_perhour_shifted_days(bird))
	max_shift = 4
	sort_shift = slow_or_fast(bird)
	
	# test input
	#X_train = np.array([[1,1,1,1,1,1],[2,2,2,2,2,2],[3,3,3,3,3,3],[4,4,4,4,4,4],[5,5,5,5,5,5],[6,6,6,6,6,6]])
	#X_test = np.array([[2,2,2,2,2,2],[11,12,11,11,11,11],[33,44,55,44,33,34]])
	
	# get anomaly prediction
	
	j = 0
	for j in range(j,max_shift+1):
		print "****************************"
		print "Test for shift: ", j+1, "hour"
		X_test_shifted = shift_all_lists(X_test, j, sort_shift)
		X_test_best = np.array(X_test_shifted)
		anomalylist = []
		anomalylist = anomaly_list(X_train, X_test_best)
		i = 0
		for i in range(i, len(anomalylist)):
			check  = anomalylist[i]
			
			if check == "anomaly":
				print "This day is an outlier: ", i+22
				
			
		
			
	
	
	
	
if __name__ == '__main__' :
    main()
    
