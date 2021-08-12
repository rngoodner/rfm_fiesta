site_configuration = {
    'systems': [
        {
            'name': 'lassen',
            'descr': 'llnl lassen',
            'hostnames': ['lassen'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'default',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['gnu'],
                }
            ]
        },
        {
            'name': 'alie',
            'descr': 'ryan personal box',
            'hostnames': ['alie'],
            'modules_system': 'tmod4',
            'partitions': [
                {
                    'name': 'default',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['gnu'],
                }
            ]
        },
        {
            'name': 'xena',
            'descr': 'unm carc xena',
            'hostnames': ['xena'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'default',
                    'scheduler': 'squeue',
                    'launcher': 'mpirun',
                    'environs': ['gnu'],
                    'resources': [
                       {
                           'name': 'gpu',
                           'options': ['--gres=gpu:{num_gpus_per_node}']
                       },
                       {
                           'name': 'partition',
                           'options': ['--partition={partition}']
                       },
                    ],
                }
            ]
        },
    ],
    'environments': [
        {
            'name': 'gnu',
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran'
        },
    ],
    'logging': [
        {
            'level': 'debug',
            'handlers': [
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s'
                },
                {
                    'type': 'file',
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: %(check_info)s: %(message)s',   # noqa: E501
                    'append': False
                },
            ],
            'handlers_perflog': [
                {
                    'type': 'filelog',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': (
                        '%(check_job_completion_time)s|reframe %(version)s|'
                        '%(check_info)s|jobid=%(check_jobid)s|'
                        '%(check_perf_var)s=%(check_perf_value)s|'
                        'ref=%(check_perf_ref)s '
                        '(l=%(check_perf_lower_thres)s, '
                        'u=%(check_perf_upper_thres)s)|'
                        '%(check_perf_unit)s'
                    ),
                    'append': True
                },
                {
                    'type': 'graylog',
                    'address': '0.0.0.0:12201',
                    'level': 'info',
                    'format': '%(message)s',
                    'extras': {
                        'facility': 'reframe',
                        'data-version': '1.1',
                    }
                },
            ]
        }
    ],
    'schedulers' : [
        {
            'name': 'squeue',
            'target_systems' : ['xena'],
            'use_nodes_option': True
        },
    ],
}
