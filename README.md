# ReFrame tests for FIESTA

## Running the tests

1. Clone this repo at the same directory level as fiesta.
1. `reframe -c fiestatest.py -C settings.py -r --performance-report`

## Supported systems

- Xena
- Lassen (must be run from an interactive session with 4 nodes)

## Requirements

- `spack install reframe`
- `spack load reframe`
