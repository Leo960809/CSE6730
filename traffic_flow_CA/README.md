# Cellular Automata Model

Author          : Jinhao Jiang

Affiliation          : Georgia Institute of Technology


Description
-------------

The corridor is modeled as a cellular automata where each section of the street is modeled as a cell that is either empty, or contains a single vehicle. Vehicles move from cell to cell in traveling through the road network using certain movement rules that are encoded into the simulation. The simulator uses a time-stepped approach to advance simulation time.


Execution
-----------

Running the simulation using

    python3 simulator.py (--num_sim <times-to-run> --L <total-length> --num_iters <timesteps-to-run> --v_max <maximum-velocity> --p <erratic-behavior-parameter>)

For plotting the traffic flow, use

    python3 plot.py (--L <total-length> --num_iters <timesteps-to-run> --v_max <maximum-velocity> --p <erratic-behavior-parameter>)
    
For input validation for empirical distribution, running

    python3 input_validation.py (--test <percentage-for-testing-set>)
