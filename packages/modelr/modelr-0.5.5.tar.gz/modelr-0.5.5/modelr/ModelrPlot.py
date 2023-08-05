
from modelr.web.urlargparse import SendHelp, ArgumentError, \
     URLArgumentParser

 
class ModelrPlot(object):

    def __init__(self, plot_json, namespace):

        # Parse additional arguments that may be required by the
        # script
        
        add_arguments = namespace['add_arguments']
        short_description = namespace.get('short_description',
                                                  'No description')

        parser = URLArgumentParser(short_description)
        add_arguments(parser)
        try:
            args = parser.parse_params(plot_json)
        except SendHelp as helper:
            raise SendHelp

        self.args = args
        self.script = namespace['run_script']
    
    def go(self, seismic_model, earth_model):

        self.plot = self.script(earth_model,
                                seismic_model,
                                self.args)
        
