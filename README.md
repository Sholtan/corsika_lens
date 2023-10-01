# corsika_lens
package for reading corsika Cherenkov output file for IVGSHAL experiment

Usage:

file_path = "CER001000-tel001"
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
