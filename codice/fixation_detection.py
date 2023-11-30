import numpy as np
import pandas as pd
from scipy.spatial import distance

def fixation(x, y, time, maxdist, mindur):
	
	"""Detects fixations, defined as consecutive samples with an inter-sample
	distance of less than a set amount of pixels (disregarding missing data)
	
	arguments

	x		-	numpy array of x positions
	y		-	numpy array of y positions
	time		-	numpy array of EyeTribe timestamps

	keyword arguments

	maxdist	-	maximal inter sample distance in pixels (default = 25)
	mindur	-	minimal duration of a fixation in milliseconds; detected
				fixation cadidates will be disregarded if they are below
				this duration (default = 100)
	
	returns
	Sfix, Efix
				Sfix	-	list of lists, each containing [starttime]
				Efix	-	list of lists, each containing [starttime, endtime, duration, endx, endy]
	"""

	# empty list to contain data
	Sfix = []
	Efix = []
	
	# loop through all coordinates
	si = 0
	fixstart = False
	for i in range(1,len(x)):
		# calculate Euclidean distance from the current fixation coordinate
		# to the next coordinate
		squared_distance = ((x[si]-x[i])**2 + (y[si]-y[i])**2)
		dist = 0.0
		if squared_distance > 0:
			dist = squared_distance**0.5
		# check if the next coordinate is below maximal distance
		if dist <= maxdist and not fixstart:
			# start a new fixation
			si = 0 + i
			fixstart = True
			Sfix.append([time[i]])
		elif dist > maxdist and fixstart:
			# end the current fixation
			fixstart = False
			# only store the fixation if the duration is ok
			if time[i-1]-Sfix[-1][0] >= mindur: #and time[i-1]-Sfix[-1][0] <=1:
				Efix.append([Sfix[-1][0], time[i-1], time[i-1]-Sfix[-1][0], x[si], y[si]])
			# delete the last fixation start if it was too short
			else:
				Sfix.pop(-1)
			si = 0 + i
		elif not fixstart:
			si += 1
	#add last fixation end (we can lose it if dist > maxdist is false for the last point)
	if len(Sfix) > len(Efix):
		Efix.append([Sfix[-1][0], time[len(x)-1], time[len(x)-1]-Sfix[-1][0], x[si], y[si]])
	return Efix



#idt veloce salvucci
def idt(x, y, time, dispersion_threshold, duration_threshold):
    fixations = []
    points = np.array(list(zip(x, y, time)))

    while points.shape[0] > 0:
        window = points[:duration_threshold, :]
        x_values = window[:, 0]
        y_values = window[:, 1]

        dispersion = (np.max(x_values) - np.min(x_values)) + (np.max(y_values) - np.min(y_values))

        if dispersion <= dispersion_threshold:
            while dispersion <= dispersion_threshold and window.shape[0] < points.shape[0]:
                window = np.vstack((window, points[window.shape[0], :]))
                x_values = window[:, 0]
                y_values = window[:, 1]
                dispersion = (np.max(x_values) - np.min(x_values)) + (np.max(y_values) - np.min(y_values))

            if window.shape[0] >= duration_threshold:  # Assicurati che ci siano almeno due punti in finestra
                centroid_time = np.mean(window[:, 2])
                start_time = window[0, 2]
                end_time = window[-1, 2]
                duration = end_time - start_time
                pos_x = np.mean(window[:, 0])
                pos_y = np.mean(window[:, 1])

                fixations.append((start_time, end_time, duration, pos_x, pos_y))

            points = points[window.shape[0]:, :]
        else:
            points = points[1:, :]

    return fixations


def idtlento(x, y, t, dispersion, duration):
    fixations = []
    
    start = 0  # Posizione iniziale della finestra
    
    while start <= len(x) - duration:
        end = start + duration  # Posizione finale della finestra
        
        # Creazione della finestra
        x_win = x[start:end]
        y_win = y[start:end]
        
        # Calcolo della dispersione
        D = (np.max(x_win, axis=0) - np.min(x_win, axis=0)) + \
            (np.max(y_win, axis=0) - np.min(y_win, axis=0))
        
        j = 1  # Espansore della finestra
        
        while D <= dispersion and end + j < len(x):
            # Espansione della finestra
            x_win = x[start:(end + j)]
            y_win = y[start:(end + j)]
            
            D = (np.max(x_win, axis=0) - np.min(x_win, axis=0)) + \
                (np.max(y_win, axis=0) - np.min(y_win, axis=0))
            
            if D > dispersion:
                # Selezione della finestra (j - 1) come fissazione
                fixations.append([t[start], t[end + j - 1], t[end + j - 1] - t[start], np.mean(x_win[:-1]), np.mean(y_win[:-1])])
                start = end + j  # Salta i punti della finestra
                break
            elif end + j == len(x):
                # Gestisci l'ultima finestra se i dati terminano durante una fissazione
                fixations.append([t[start], t[end], t[end] - t[start], np.mean(x_win), np.mean(y_win)])
                start = end + j
                break
            
            j += 1
        
        start += 1
    
    return fixations





def calculate_velocity(x, y, time):
    # Calculate point-to-point velocities
    dx = np.diff(x)
    dy = np.diff(y)
    dt = np.diff(time)
    velocities = np.sqrt(dx**2 + dy**2) / dt
    velocities = np.insert(velocities, 0, 0)  # Insert 0 for the first point

    return velocities

#ivt salvucci
def ivta(x, y, time, vel_threshold):
    fixations = []

    # Calculate point-to-point velocities
    velocities = [((x[i+1] - x[i])**2 + (y[i+1] - y[i])**2) / (time[i+1] - time[i]) for i in range(len(x)-1)]

    # Label each point below velocity threshold as fixation, otherwise as saccade
    labels = ['fixation' if v < vel_threshold else 'saccade' for v in velocities]

    # Collapse consecutive fixation points into fixation groups
    fixation_groups = []
    current_group = []
    for i, label in enumerate(labels):
        current_group.append(i)
        if i == len(labels) - 1 or labels[i+1] == 'saccade':
            if current_group:
                fixation_groups.append(current_group)
                current_group = []

    # Map each fixation group to a fixation at the centroid of its points
    for group in fixation_groups:
        start_time = time[group[0]]
        end_time = time[group[-1]]
        duration = end_time - start_time

        if duration >= 0.2:
            centroid_x = sum(x[i] for i in group) / len(group)
            centroid_y = sum(y[i] for i in group) / len(group)

            fixations.append((start_time,end_time,duration,centroid_x,centroid_y))

    return fixations


#ivt salvucci nuovo
def ivt(x, y, time, velocity_threshold):
    # Calculate velocities
    velocities = calculate_velocity(x, y, time)

    # Label points as fixation or saccade
    labels = np.where(velocities <= velocity_threshold, 'Fixation', 'Saccade')

    # Collapse consecutive fixation points into fixation groups
    fixation_groups = []
    current_group = []
    for i, label in enumerate(labels):
        if label == 'Fixation':
            current_group.append(i)
        else:
            if current_group:
                fixation_groups.append(current_group)
                current_group = []

    # Map each fixation group to a fixation at the centroid
    fixations = []
    for group in fixation_groups:
        group_x = x[group]
        group_y = y[group]
        start_time = time[group[0]]
        end_time = time[group[-1]]
        duration = end_time - start_time
        if duration >= 0.2:
            centroid_x = np.mean(group_x)
            centroid_y = np.mean(group_y)
            fixations.append((start_time, end_time, duration, centroid_x, centroid_y))

    return fixations





