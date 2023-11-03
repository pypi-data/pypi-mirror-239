#!/usr/bin/env python
# coding=utf-8
# -------------------------------------------------------------------------------
#
#  ███████╗██████╗ ██╗ ██████╗███████╗██╗     ██╗██████╗
#  ██╔════╝██╔══██╗██║██╔════╝██╔════╝██║     ██║██╔══██╗
#  ███████╗██████╔╝██║██║     █████╗  ██║     ██║██████╔╝
#  ╚════██║██╔═══╝ ██║██║     ██╔══╝  ██║     ██║██╔══██╗
#  ███████║██║     ██║╚██████╗███████╗███████╗██║██████╔╝
#  ╚══════╝╚═╝     ╚═╝ ╚═════╝╚══════╝╚══════╝╚═╝╚═════╝
#
# Name:        worst_case.py
# Purpose:     Classes to automate Worst-Case simulations
#
# Author:      Nuno Brum (nuno.brum@gmail.com)
#
# Created:     10-08-2023
# Licence:     refer to the LICENSE file
# -------------------------------------------------------------------------------

import logging
from typing import Union, Callable, Type
from ...log.logfile_data import LogfileData
from ..process_callback import ProcessCallback
from .tolerance_deviations import ToleranceDeviations, DeviationType

_logger = logging.getLogger("spicelib.SimAnalysis")


class WorstCaseAnalysis(ToleranceDeviations):
    """Class to automate Monte-Carlo simulations"""

    def _set_component_deviation(self, ref: str, index) -> bool:
        """Sets the deviation of a component. Returns True if the component is valid and the deviation was set.
        Otherwise, returns False"""
        val, dev = self.get_component_value_deviation_type(ref)  # get there present value
        if dev.min_val == dev.max_val:
            return False  # no need to set the deviation
        new_val = val
        if dev.typ == DeviationType.tolerance:
            new_val = "{wc(%s,%g,%d)}" % (val, dev.max_val, index)  # calculate expression for new value
        elif dev.typ == DeviationType.minmax:
            new_val = "{wc1(%s,%g,%g,%d)}" % (val, dev.min_val, dev.max_val, index)  # calculate expression for new value

        if new_val != val:
            self.set_component_value(ref, new_val)  # update the value
        return True

    def prepare_testbench(self, **kwargs):
        """Prepares the simulation by setting the tolerances for the components"""
        index = 0
        for ref in self.device_deviations:
            if self._set_component_deviation(ref, index):
                index += 1
        for ref in self.parameter_deviations:
            val, dev = self.get_parameter_value_deviation_type(ref)
            new_val = val
            if dev.typ == DeviationType.tolerance:
                new_val = "{wc(%s,%g,%d)}" % (val, dev.max_val, index)  # calculate expression for new value
            elif dev.typ == DeviationType.minmax:
                new_val = "{wc1(%s,%g,%g,%d)}" % (val, dev.min_val, dev.max_val, index)
            if new_val != val:
                self.editor.set_parameter(ref, new_val)
            index += 1

        for prefix in self.default_tolerance:
            for ref in self.get_components(prefix):
                if ref not in self.device_deviations:
                    if self._set_component_deviation(ref, index):
                        index += 1

        self.editor.add_instruction(".func binary(run,idx) floor(run/(2**idx))-2*floor(run/(2**(idx+1)))")
        self.editor.add_instruction(".func wc(nom,tol,idx) {nom*if(binary(run,idx),1-tol,1+tol)}")
        self.editor.add_instruction(".func wc1(nom,min,max,idx) {nom*if(binary(run,idx),min,max)}")
        self.num_runs = 2**index - 1
        self.editor.add_instruction(".step param run -1 %d 1" % self.num_runs)
        self.editor.set_parameter('run', -1)  # in case the step is commented.
        self.testbench_prepared = True

    def run_analysis(self,
                     callback: Union[Type[ProcessCallback], Callable] = None,
                     callback_args: Union[tuple, dict] = None,
                     switches=None,
                     timeout: float = None,
                     ):
        """This method runs the analysis without updating the netlist.
        It will update component values and parameters according to their deviation type and call the simulation.
        The advantage of this method is that it doesn't require adding random functions to the netlist.
        The number of times the simulation is done is specified on the argument num_runs."""
        self.clear_simulation_data()
        # Calculate the number of runs

        worst_case_elements = {}
        worst_case_index = []

        def check_and_add_component(ref: str):
            val, dev = self.get_component_value_deviation_type(ref)  # get there present value
            if dev.min_val == dev.max_val or dev.typ == DeviationType.none:
                return
            worst_case_elements[ref] = val, dev, 'component'
            worst_case_index.append(ref)

        for ref in self.device_deviations:
            check_and_add_component(ref)

        for ref in self.parameter_deviations:
            val, dev = self.get_parameter_value_deviation_type(ref)
            if dev.typ == DeviationType.tolerance or dev.typ == DeviationType.minmax:
                worst_case_elements[ref] = val, dev, 'parameter'
                worst_case_index.append(ref)

        for prefix in self.default_tolerance:
            for ref in self.get_components(prefix):
                if ref not in self.device_deviations:
                    check_and_add_component(ref)

        num_runs = 2**len(worst_case_index) - 1
        if num_runs > 4096:
            _logger.warning("The number of runs is too high. It will be limited to 4096\n"
                            "Consider limiting the number of components with deviation")
            return

        self._reset_netlist()  # reset the netlist
        self.play_instructions()  # play the instructions
        last_run = 2 ** len(worst_case_index) - 1  # Sets all valid bits to 1
        for run in range(num_runs):
            # Preparing the variation on components, but only on the ones that have changed
            bit_updated = run ^ last_run
            bit_index = 0
            while bit_updated != 0:
                if bit_updated & 1:
                    ref = worst_case_index[bit_index]
                    val, dev, typ = worst_case_elements[ref]
                    if dev.typ == DeviationType.tolerance:
                        new_val = val * (1 - dev.max_val) if run & (1 << bit_index) else val * (1 + dev.max_val)
                    elif dev.typ == DeviationType.minmax:
                        new_val = dev.min_val if run & (1 << bit_index) else dev.max_val
                    else:
                        _logger.warning("Unknown deviation type")
                        new_val = val
                    if typ == 'component':
                        self.editor.set_component_value(ref, new_val)  # update the value
                    elif typ == 'parameter':
                        self.editor.set_parameter(ref, new_val)
                    else:
                        _logger.warning("Unknown type")
                bit_updated >>= 1
                bit_index += 1
            # Run the simulation
            self.run(self.editor, wait_resource=True,
                     callback=callback, callback_args=callback_args,
                     switches=switches, timeout=timeout)
            last_run = run
        self.runner.wait_completion()

        if callback is not None:
            callback_rets = []
            for rt in self.simulations:
                callback_rets.append(rt.get_results())
            self.simulation_results['callback_returns'] = callback_rets

    def get_min_max_measure_value(self, meas_name: str):
        if 'log_data' not in self.simulation_results:
            log_data = self.read_logfiles()
            self.simulation_results['log_data'] = log_data

        log_data: LogfileData = self.simulation_results['log_data']
        meas_data = log_data[meas_name]
        if meas_data is None:
            _logger.warning("Measurement %s not found in log files", meas_name)
            return None
        else:
            return min(meas_data), max(meas_data)

    def make_sensitivity_analysis(self, meas_name: str, ref: str):
        """Makes a sensitivity analysis for a given measurement and reference component"""
        pass
        # TODO: implement this method
        # 1. Run the simulation
        # 2. Read the log files
        # 3. Calculate the sensitivity
