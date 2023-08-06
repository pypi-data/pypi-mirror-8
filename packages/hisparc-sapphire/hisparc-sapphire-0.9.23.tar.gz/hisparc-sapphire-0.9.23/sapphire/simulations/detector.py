"""Common HiSPARC station response simulations

These are some common simulations for HiSPARC detectors.

"""
from math import sqrt, acos, pi
import random

import numpy as np

from .base import BaseSimulation
from ..utils import ceil_in_base


class HiSPARCSimulation(BaseSimulation):

    def simulate_detector_offsets(self, n_detectors):
        """Get multiple detector offsets

        :param n_detectors: number of offsets to return.

        """
        return [self.simulate_detector_offset() for _ in range(n_detectors)]

    def simulate_detector_offset(self):
        """Simulate time offsets between detectors in one station

        This offset should be fixed for each detector for a simulation run.

        """
        return np.random.normal(0, 2.77)

    def simulate_station_offset(self):
        """Simulate time offsets between different stations

        This offset should be fixed for each station for a simulation run.
        The actual distribution is not yet very clear. We assume it is
        gaussian for convenience. Then the stddev is about 16 ns.

        """
        return np.random.normal(0, 16)

    def simulate_gps_uncertainty(self):
        """Simulate uncertainty from GPS receiver"""

        return np.random.normal(0, 4.5)

    def simulate_adc_sampling(self, t):
        """Simulate ADC time binning due to the sampling frequency

        :param t: time to be binned.
        :returns: time ceiled in 2.5 ns base.

        """
        return ceil_in_base(t, 2.5)

    def simulate_signal_transport_time(self, n=1):
        """ Simulate transport times of scintillation light to the PMT

        Generates random transit times within a given distribution and
        adds it to the times the particles passed the detector.

        Be careful when editting this function, be sure to check both
        the single and vectorized part.

        :param n: number of times to simulate
        :returns: list of signal transport times

        """
        numbers = np.random.random(n)
        if n < 20:
            dt = np.array([2.5507 + 2.39885 * number if number < 0.39377 else
                           1.56764 + 4.89536 * number for number in numbers])
        else:
            dt = np.where(numbers < 0.39377,
                          2.5507 + 2.39885 * numbers,
                          1.56764 + 4.89536 * numbers)
        return dt

    def simulate_detector_mips(self, particles):
        """Simulate the detector signal response for particles

        :param particles: an array of particle rows.

        """
        if len(particles) < 4:
            mips = sum(self.simulate_detector_mip(p) for p in particles)
        else:
            mips = sum(self.simulate_detector_mip(particles))

        return mips

    def simulate_detector_mip(self, particle):
        """Simulate the detector signal for particles

        Be careful when editting this function, be sure to check both
        the single and vectorized part.

        :param particle: particle row or rows with the p_[x, y, z]
                         components of the particle momentum.

        """

        # Simulation of convoluted distribution of electron and
        # muon energy losses with the scintillator response
        if particle.ndim == 0:
            # determination of lepton angle of incidence
            costheta = abs(particle['p_z']) / sqrt(particle['p_x'] ** 2 +
                                                   particle['p_y'] ** 2 +
                                                   particle['p_z'] ** 2)

            y = np.random.random()

            if y < 0.3394:
                mip = (0.48 + 0.8583 * sqrt(y)) / costheta
            elif y < 0.4344:
                mip = (0.73 + 0.7366 * y) / costheta
            elif y < 0.9041:
                mip = (1.7752 - 1.0336 * sqrt(0.9267 - y)) / costheta
            else:
                mip = (2.28 - 2.1316 * sqrt(1 - y)) / costheta
        else:
            # determination of lepton angle of incidence
            costheta = abs(particle['p_z']) / np.sqrt(particle['p_x'] ** 2 +
                                                      particle['p_y'] ** 2 +
                                                      particle['p_z'] ** 2)
            y = np.random.random(len(particle))

            mip = np.where(y < 0.3394,
                           (0.48 + 0.8583 * np.sqrt(y)) / costheta,
                           (0.73 + 0.7366 * y) / costheta)
            mip = np.where(y < 0.4344, mip,
                           (1.7752 - 1.0336 * np.sqrt(0.9267 - y)) / costheta)
            mip = np.where(y < 0.9041, mip,
                           (2.28 - 2.1316 * np.sqrt(1 - y)) / costheta)

        return mip

    def generate_zenith(self):
        """Generate a random zenith

        Pick from the expected zenith distribution.

        TODO: There is a difference between expected shower zeniths
        detected on the ground and at the top of the atmosphere. So
        simulations that use CORSIKA generated showers need to take that
        into account.

        """
        p = np.random.random()
        return self.inverse_zenith_probability(p)

    def inverse_zenith_probability(self, p):
        """Inverse cumulative probability distribution for zenith

        Derrived from Schultheiss "The acceptancy of the HiSPARC Network",
        (internal note), eq 2.4 from Rossi.

        :param p: probability value between 0 and 1.
        :returns: zenith with corresponding cumulative probability.

        """
        return acos((1 - p) ** (1 / 8.))

    def generate_azimuth(self):
        """Generate a random azimuth

        Showers from each azimuth have equal probability

        """
        return np.random.uniform(-pi, pi)


class ErrorlessSimulation(HiSPARCSimulation):

    def simulate_detector_offsets(self, n_detectors):

        return [0.] * n_detectors

    def simulate_detector_offset(self):

        return 0.

    def simulate_station_offset(self):

        return 0.

    def simulate_gps_uncertainty(self):

        return 0.

    def simulate_adc_sampling(self, t):

        return t

    def simulate_signal_transport_time(self, n=1):

        return np.array([0.] *  n)

    def simulate_detector_mips(self, particles):

        return len(particles)

    def simulate_detector_mip(self, particle):

        return 1.
