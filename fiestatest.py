import reframe as rfm
import reframe.utility.sanity as sn
import os

LAUNCHDIR = os.getcwd()

@rfm.simple_test
class FiestaTest(rfm.RegressionTest):
	valid_systems = ['lassen','xena']
	valid_prog_environs = ['gnu']
	sourcesdir = '../fiesta/'
	sourcepath = '.'
	executable = './build/fiesta'
	executable_opts = [f'{LAUNCHDIR}/3D_Expansion_small_gpu-type/fiesta.lua', '--kokkos-num-devices=1']
	build_system = 'CMake'
	num_tasks = 4
	num_tasks_per_node = 1
	time_limit = '0d0h15m0s'

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
		if system == 'xena':
			self.modules = [
				'gcc/10.2.0-3kjq',
				'intel-mpi/2020.2.254-rxha',
				'cuda/11.2.0-w6mf',
				'cmake/3.19.5-22ub',
				'hdf5/1.10.7-pvyi'
			]

	@run_before('run')
	def set_other_system_options(self):
		system = self.current_system.name
		if system == 'xena':
			self.extra_resources = {
				'gpu': {'num_gpus_per_node': '1'},
				'partition': {'partition': 'singleGPU'}
			}
		
		# this is a bit of a hack to work around reframe not supporting lsf
		# tests for lassen must be run from an interactive session with 4 nodes
		if system == 'lassen':
			self.executable = 'lrun'
			self.executable_opts = ['-N4', '-T1', './build/fiesta', f'{LAUNCHDIR}/3D_Expansion_small_gpu-type/fiesta.lua', '--kokkos-num-devices=1']
