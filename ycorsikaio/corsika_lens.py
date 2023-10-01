#!/usr/bin/env python3
import numpy as np

import matplotlib.pyplot as plt






class Corsika_event:
	rad_to_degree = 180./np.pi
	def __init__(self, event, detector_center, lense_radius, telescope_number):
		print("\nreading event")

		self.telescope_number = telescope_number

		self.header = event.header
		self.run_number = self.header["run_number"]
		self.event_number = self.header["event_number"]


		self.photons = event.photons
		self.detector_center = detector_center      # in centimeters
		self.lense_radius = lense_radius            # in centimeters



		self.zenith = self.header["zenith"]
		self.azimuth = self.header["azimuth"]
		print("zenith angle in degrees:", self.zenith * self.rad_to_degree)
		print("azimuth angle in degrees:", self.azimuth * self.rad_to_degree)
		
		self.bunches_n = len(self.photons)
		print("bunches in event:", self.bunches_n, "\n")

		
		self.w = -np.sqrt(1 - (self.photons['u'])*(self.photons['u']) - (self.photons['v'])*(self.photons['v']))
		
		self._define_shower_axis()
		self._calculate_lens_cors_coords()
		self._define_lens_axis_vectors()
		self._calculate_lens_own_coords()
		self._calculate_directional_cos_in_lens_system()

	def _calculate_directional_cos_in_lens_system(self):
		self.u_lens = self.photons['u'] * self.lens_x_axis_vector['x'] + self.photons['v'] * self.lens_x_axis_vector['y'] + self.w * self.lens_x_axis_vector['z']
		self.v_lens = self.photons['u'] * self.lens_y_axis_vector['x'] + self.photons['v'] * self.lens_y_axis_vector['y'] + self.w * self.lens_y_axis_vector['z']
		self.w_lens = self.photons['u'] * self.lens_z_axis_vector['x'] + self.photons['v'] * self.lens_z_axis_vector['y'] + self.w * self.lens_z_axis_vector['z']

	def _calculate_lens_own_coords(self):
		self.x_lens_own = (self.x_of_lens_cors_coords - self.detector_center['x']) * self.lens_x_axis_vector['x'] + (self.y_of_lens_cors_coords - self.detector_center['y']) * self.lens_x_axis_vector['y']
		self.y_lens_own = (self.x_of_lens_cors_coords - self.detector_center['x']) * self.lens_y_axis_vector['x'] + (self.y_of_lens_cors_coords - self.detector_center['y']) * self.lens_y_axis_vector['y'] + (self.z_of_lens_cors_coords - self.detector_center['z']) * self.lens_y_axis_vector['z']
		self.z_lens_own = (self.x_of_lens_cors_coords - self.detector_center['x']) * self.lens_z_axis_vector['x'] + (self.y_of_lens_cors_coords - self.detector_center['y']) * self.lens_z_axis_vector['y'] + (self.z_of_lens_cors_coords - self.detector_center['z']) * self.lens_z_axis_vector['z']

	def _define_shower_axis(self):
		self.shower_axis = {'x':np.sin(self.zenith)*np.cos(self.azimuth), 'y':np.sin(self.zenith)*np.sin(self.azimuth), 'z':-np.cos(self.zenith)}


	def _define_lens_axis_vectors(self):
		self.lens_x_axis_vector = {'x':np.sin(self.azimuth), 'y':-np.cos(self.azimuth), 'z':0}
		self.lens_y_axis_vector = {'x':np.cos(self.zenith)*np.cos(self.azimuth), 'y':np.cos(self.zenith)*np.sin(self.azimuth), 'z':np.sin(self.zenith)}
		self.lens_z_axis_vector = {'x':np.sin(self.zenith)*np.cos(self.azimuth), 'y':np.sin(self.zenith)*np.sin(self.azimuth), 'z':-np.cos(self.zenith)}

	def _calculate_lens_cors_coords(self):
		p_numerator = self.shower_axis['x'] * (self.photons['x'] - self.detector_center['x']) + self.shower_axis['y'] * (self.photons['y'] - self.detector_center['y']) + self.shower_axis['z'] * (-self.detector_center['z'])
		p_divisor = self.shower_axis['x'] * (self.photons['u']) + self.shower_axis['y'] * (self.photons['v']) + self.shower_axis['z'] * (self.w)

		p = -p_numerator/p_divisor    # also gives the distance photon traveled from lens to ground

		self.x_of_lens_cors_coords = self.photons['x'] + self.photons['u'] * p
		self.y_of_lens_cors_coords = self.photons['y'] + self.photons['v'] * p
		self.z_of_lens_cors_coords = self.w * p

	def add_plot_3d(self):
		print("\n3d plot in corsika coordinate system")

		fig = plt.figure()
		ax = fig.add_subplot(projection='3d')
		z = np.zeros(self.bunches_n)
		ax.scatter(self.photons['x'], self.photons['y'], z, marker = 'o')
		ax.scatter(self.x_of_lens_cors_coords, self.y_of_lens_cors_coords, self.z_of_lens_cors_coords, marker = '^')
		#ax.scatter(np.concatenate((self.photons['x'], self.x_of_lens_cors_coords)), np.concatenate((self.photons['y'],self.y_of_lens_cors_coords)), np.concatenate((z,self.z_of_lens_cors_coords)))

		q = np.array(range(45, 200))

		xaxis_x = self.detector_center['x'] + q*self.lens_x_axis_vector['x']
		xaxis_y = self.detector_center['y'] + q*self.lens_x_axis_vector['y']
		xaxis_z = self.detector_center['z'] + q*self.lens_x_axis_vector['z']
		ax.scatter(xaxis_x, xaxis_y, xaxis_z, marker = '*')

		yaxis_x = self.detector_center['x'] + q*self.lens_y_axis_vector['x']
		yaxis_y = self.detector_center['y'] + q*self.lens_y_axis_vector['y']
		yaxis_z = self.detector_center['z'] + q*self.lens_y_axis_vector['z']
		ax.scatter(yaxis_x, yaxis_y, yaxis_z, marker = '*')

		q = np.array(range(0, 155))

		zaxis_x = self.detector_center['x'] + q*self.lens_z_axis_vector['x']
		zaxis_y = self.detector_center['y'] + q*self.lens_z_axis_vector['y']
		zaxis_z = self.detector_center['z'] + q*self.lens_z_axis_vector['z']
		ax.scatter(zaxis_x, zaxis_y, zaxis_z, marker = '*')

		ax.set_xlabel('X Label')
		ax.set_ylabel('Y Label')
		ax.set_zlabel('Z Label')
		ax.axis('equal')
		#plt.show()

	def add_plot_2d(self):
		print("\n2d plot in lens coordinate system")

		fig2 = plt.figure()
		ax2 = fig2.add_subplot()

		ax2.scatter(self.x_lens_own, self.y_lens_own)
		ax2.set_xlabel('X Label')
		ax2.set_ylabel('Y Label')
		ax2.axis('equal')

		#plt.show()

	def write_txt(self, path):
		print("writing photons file")

		distance_from_det_center = np.sqrt(self.x_lens_own*self.x_lens_own + self.y_lens_own*self.y_lens_own)
		mask = distance_from_det_center < 41.

		z_to_write = np.full(self.bunches_n, -0.1)

		x_lens_own_meters = self.x_lens_own/100.
		y_lens_own_meters = self.y_lens_own/100.

		data_to_write = np.column_stack((x_lens_own_meters[mask], y_lens_own_meters[mask], z_to_write[mask], self.u_lens[mask], self.v_lens[mask], self.w_lens[mask], self.photons['wavelength'][mask]))
		header = "x [m], y [m], z [m], u, v, w, wavelength [nm]"

		name_to_write = self.telescope_number + "_z_" + str(round(self.zenith * self.rad_to_degree)) +"_run_" + str(int(self.run_number)) + "_event_" + str(int(self.event_number)) + "_photons" + ".txt"

		run_dir = "run_"+str(int(self.run_number))+'/'

		np.savetxt(path + run_dir + name_to_write, data_to_write, delimiter='\t', header=header, comments='%')










