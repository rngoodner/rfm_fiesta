import reframe as rfm
import reframe.utility.sanity as sn
import os

LAUNCHDIR = os.getcwd()

@rfm.simple_test
class FiestaTest(rfm.RegressionTest):
	def __init__(self):
		self.valid_systems = ['lassen']
		self.valid_prog_environs = ['gnu']
		self.sourcesdir = '../fiesta/'
		self.sourcepath = '.'
		self.executable = 'lrun'
		self.executable_opts = ['-N2', '-T4', './build/fiesta', f'{LAUNCHDIR}/3D_Expansion_small_gpu-type/fiesta.lua --kokkos-num-devices=4']
		self.build_system = 'CMake'

	@run_before('compile')
	def set_compiler_flags(self):
		self.build_system.cppflags = ['-DCUDA=ON']
		self.build_system.builddir = 'build'

	@run_before('sanity')
	def set_sanity_patterns(self):
		self.sanity_patterns = sn.assert_found('Simulation Complete!', self.stdout)
	
	@run_before('compile')
	def load_modules(self):
		system = self.current_system.name
		if system == 'lassen':
			self.modules = [
				'gcc/8.3.1',
				'lrun/2020.03.05',
				'spectrum-mpi/rolling-release',
				'cuda/11.1.1',
				'cmake/3.14.5',
				'hdf5-parallel/1.10.4'
			]
