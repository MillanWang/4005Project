class Logger:
    __enable_inspector_logging = True
    __enable_workstation_logging = True

    # In the future, python Logging module will be used to log messages to an output file, this flag will indicate if file logging is enabled or not. 
    __create_log_files = True

    def __init__(self, enable_inspector_logging, enable_workstation_logging, create_log_files):
        self.__enable_inspector_logging = enable_inspector_logging
        self.__enable_workstation_logging = enable_workstation_logging
        self.__create_log_files = create_log_files

    def log_inspector_component_selection(component, time):
        if Logger.__enable_inspector_logging == True:
            print("The inspector has started inspecting " + component.name + " at " + time + "s")
        else:
            return

    def log_inspector_buffered_component(component, workstation, time):
        if Logger.__enable_inspector_logging == True:
            print("The inspector has placed " + component.name + " in " + workstation.name + "'s buffer at " + time + "s")
        else:
            return

    def log_workstation_unbuffer(workstation, component, time):
        if Logger.__enable_workstation_logging == True:
            print(component.name + " has entered " + workstation.name + " at time " + time + "s")
        else:
            return
    
    def log_product_created(product, time):
        if Logger.__enable_workstation_logging == True:
            print(product.name + " has been completed at " + time + "s")
        else:
            return




