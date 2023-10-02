#!/usr/bin/env python3
import numpy as np

import matplotlib.pyplot as plt

from ycorsikaio import Corsika_event
from ycorsikaio import CorsikaCherenkovFile



def draw_any_hist(some_array, bin_n = 100, xlabel = '???', title='???', range=None):
	fig3 = plt.figure()
	ax3 = fig3.add_subplot()
	ax3.hist(some_array, bins=bin_n, range=range)
	ax3.set_title(title, fontsize=22)
	ax3.set_xlabel(xlabel, fontsize=22)


	mean = np.mean(some_array)
	std = np.std(some_array)

	plt.text(0.05, 0.95, f"Mean: {mean:.2f}\nStd: {std:.2f}", transform=plt.gca().transAxes, va='top', fontsize=22)

	plt.show()



def cer_to_txt(run_number, telescope_number, detector_center):
	file_path = "run_" + run_number + "/CER00" + run_number + "-" + telescope_number
	events = []
	with CorsikaCherenkovFile(file_path) as f:
		print("reading file:", file_path)
		print("run_number:", f.run_header['run_number'])
		for event in f:
			events.append(Corsika_event(event, detector_center, lense_radius, telescope_number))
	print("events in a run:", len(events))
	for event in events:
		event.write_txt(path = "txts/")
		#event.add_plot_3d()
		#event.add_plot_2d()
		#plt.show()




lense_radius = 41.                         # in centimeters


telescope_numbers_array = ["tel001", "tel002", "tel003", "tel004", "tel005", "tel006", "tel007", "tel008", "tel009", "tel010"]
detector_centers_dict = dict()
ys = [0, 500, 1000, 2000, 4000, 8000, 10000, 12000, 15000, 20000]
for i in range(10):
	detector_centers_dict[telescope_numbers_array[i]] = {'x':0, 'y':ys[i], 'z':41}
runs = (str(1000), str(1001), str(1002), str(1003), str(1004))


for r in runs:
	for telescope_number in telescope_numbers_array:
		cer_to_txt(r, telescope_number, detector_centers_dict[telescope_number])













