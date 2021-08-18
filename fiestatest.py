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
    executable_opts = [f'{LAUNCHDIR}/3D_Expansion_small_gpu-aware/fiesta.lua', '--kokkos-num-devices=1']
    build_system = 'CMake'
    num_tasks = 4
    num_tasks_per_node = 1
    time_limit = '0d0h15m0s'
    reference = {
        '*': {
            'Total Time': (0, 0, 0, 's'),    
            'Setup Time': (0, 0, 0, 's'),
            'Initial Condition Generation': (0, 0, 0, 's'),
            'Grid Generation': (0, 0, 0, 's'),
            'Initial Condition WriteTime': (0, 0, 0, 's'),
            'Simulation Time': (0, 0, 0, 's'),
            'Flux Calculation': (0, 0, 0, 's'),
            'Secondary Variable Calculation': (0, 0, 0, 's'),
            'Solution Write Time': (0, 0, 0, 's'),
            'Runge Stage Update': (0, 0, 0, 's'),
            'Pressure Gradient Calculation': (0, 0, 0, 's'),
            'Status Check': (0, 0, 0, 's'),
            'Boundary Conditions': (0, 0, 0, 's'),
            'Halo Exchanges': (0, 0, 0, 's'),
            'Restart Write Time': (0, 0, 0, 's')
        }
    }

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
        if system == 'lassen':
            self.extra_resources = {
                'queue': {'queue': 'pbatch'}
            }
        
        # this is a bit of a hack to work around reframe not supporting lsf
        # tests for lassen must be run from an interactive session with 4 nodes
        # if system == 'lassen':
        #     self.executable = 'lrun'
        #     self.executable_opts = ['-N4', '-T1', './build/fiesta', f'{LAUNCHDIR}/3D_Expansion_small_gpu-aware/fiesta.lua', '--kokkos-num-devices=1']
    
    @run_before('performance')
    def set_perf_patterns(self):
        self.perf_patterns = {
            'Total Time': sn.extractsingle(r'Total Time:\s+(\S+).*', self.stdout, 1, float),
            'Setup Time': sn.extractsingle(r'\s+Setup Time:\s+(\S+).*', self.stdout, 1, float),
            'Initial Condition Generation': sn.extractsingle(r'\s+Initial Condition Generation:\s+(\S+).*', self.stdout, 1, float),
            'Grid Generation': sn.extractsingle(r'\s+Grid Generation:\s+(\S+).*', self.stdout, 1, float),
            'Initial Condition WriteTime': sn.extractsingle(r'\s+Initial Condition WriteTime:\s+(\S+).*', self.stdout, 1, float),
            'Simulation Time': sn.extractsingle(r'\s+Simulation Time:\s+(\S+).*', self.stdout, 1, float),
            'Flux Calculation': sn.extractsingle(r'\s+Flux Calculation:\s+(\S+).*', self.stdout, 1, float),
            'Secondary Variable Calculation': sn.extractsingle(r'\s+Secondary Variable Calculation:\s+(\S+).*', self.stdout, 1, float),
            'Solution Write Time': sn.extractsingle(r'\s+Solution Write Time:\s+(\S+).*', self.stdout, 1, float),
            'Runge Stage Update': sn.extractsingle(r'\s+Runge Stage Update:\s+(\S+).*', self.stdout, 1, float),
            'Pressure Gradient Calculation': sn.extractsingle(r'\s+Pressure Gradient Calculation:\s+(\S+).*', self.stdout, 1, float),
            'Status Check': sn.extractsingle(r'\s+Status Check:\s+(\S+).*', self.stdout, 1, float),
            'Boundary Conditions': sn.extractsingle(r'\s+Boundary Conditions:\s+(\S+).*', self.stdout, 1, float),
            'Halo Exchanges': sn.extractsingle(r'\s+Halo Exchanges:\s+(\S+).*', self.stdout, 1, float),
            'Restart Write Time': sn.extractsingle(r'\s+Restart Write Time:\s+(\S+).*', self.stdout, 1, float)
        }
