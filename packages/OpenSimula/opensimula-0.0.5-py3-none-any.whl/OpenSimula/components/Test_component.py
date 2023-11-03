from OpenSimula.Parameters import (
    Parameter_boolean,
    Parameter_float,
    Parameter_int,
    Parameter_string,
    Parameter_options,
    Parameter_component,
    Parameter_boolean_list,
    Parameter_string_list,
    Parameter_int_list,
    Parameter_float_list,
    Parameter_options_list,
    Parameter_component_list,
)
from OpenSimula.Component import Component
from OpenSimula.Variable import Variable


class Test_component(Component):
    """Component for development testing"""

    def __init__(self, name, project):
        Component.__init__(self, name, project)
        self.parameter("type").value = "Test_component"
        self.parameter("description").value = "Dummy component for testing"

        self.add_parameter(Parameter_boolean("boolean", False))
        self.add_parameter(Parameter_string("string", "Hello World"))
        self.add_parameter(Parameter_int("int", 100, "h"))
        self.add_parameter(Parameter_float("float", 0.1, "m"))
        self.add_parameter(Parameter_options("options", "One", ["One", "Two", "Three"]))
        self.add_parameter(Parameter_component("component", "not_defined"))
        self.add_parameter(Parameter_boolean_list("boolean_list", [True, False]))
        self.add_parameter(
            Parameter_string_list("string_list", ["Hello World 1", "Hello World 2"])
        )
        self.add_parameter(Parameter_int_list("int_list", [50, 100], "h"))
        self.add_parameter(Parameter_float_list("float_list", [0.1, 0.2], "m"))
        self.add_parameter(
            Parameter_options_list(
                "options_list", ["One", "Two"], ["One", "Two", "Three"]
            )
        )
        self.add_parameter(
            Parameter_component_list("component_list", ["not_defined", "not_defined"])
        )
        self._initial_date_ = None

    def pre_simulation(self, n_time_steps, delta_t):
        self.del_all_variables()
        self.add_variable(Variable("t", n_time_steps, unit="s"))
        self.print(f"Component: {self.parameter('name').value} Starting simulation ...")

    def pre_iteration(self, time_index, date):
        if time_index == 0:
            self._initial_date_ = date
        self.variable("t").array[time_index] = (
            date - self._initial_date_
        ).total_seconds()

    def post_simulation(self):
        self.print(f"Component: {self.parameter('name').value} Ending simulation ...")
