from OpenSimula.Component import Component
from OpenSimula.Parameters import Parameter_component_list
from OpenSimula.Variable import Variable


class Space(Component):
    def __init__(self, name, project):
        Component.__init__(self, name, project)
        self.parameter("type").value = "Space"
        self.parameter("description").value = "Indoor building space"
        self.add_parameter(Parameter_component_list("walls"))

    def pre_simulation(self, n_time_steps, delta_t):
        self.del_all_variables()
        self.add_variable(Variable("temperature", n_time_steps, unit="°C"))
        self.add_variable(Variable("rel_humidity", n_time_steps, unit="%"))
