class SimulationLogger:
    __enable_inspector_logging = True
    __enable_workstation_logging = True

    # In the future, python Logging module will be used to log messages to an output file, this flag will indicate if file logging is enabled or not.
    __create_log_files = True

    def __init__(self, enable_inspector_logging, enable_workstation_logging, create_log_files):
        self.__enable_inspector_logging = enable_inspector_logging
        self.__enable_workstation_logging = enable_workstation_logging
        self.__create_log_files = create_log_files

    def log_inspector_component_selection(self, component, time):
        """ Given component and time, log message when inspector starts inspecting a component """
        if self.__enable_inspector_logging == True:
            output = time + " - " + "The inspector has started inspecting " + component.name
            print(output)
        else:
            return

    def log_inspector_buffered_component(self, component, workstation, time):
        """ Given component, workstation and time, log message when insepctor moves component into a workstation's """
        if self.__enable_inspector_logging == True:
            output = time + " - " + "The inspector has placed " + component.name + " in " + workstation.name + "'s buffer"
            print(output)
        else:
            return

    def log_workstation_unbuffer(self, workstation, component, time):
        """ Given workstation, component, and time, log message when a component leaves the buffer and enters into the workstation """
        if self.__enable_workstation_logging == True:
            output = time + " - " + component.name + " has entered " + workstation.name
            print(output)
        else:
            return

    def log_product_created(self, product, time):
        """ Given a product and time, log message when a component leaves the buffer and enters into the workstation """
        if self.__enable_workstation_logging == True:
            output = time + " - " + product.name + " has been completed"
            print(output)
        else:
            return
