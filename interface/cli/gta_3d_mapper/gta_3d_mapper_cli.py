from core.servicies.gta_3d_mapper.model_service import ModelService
from config.constants import DICT_COPY_MODES

import argparse

class GTA3DMapperCLI():
    def __init__(self, model_service: ModelService):
        self.model_service = model_service

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '-m', '--mode',
            help='set copy mode of input to output. Modes: "normal", "random_counted", "random"'
        )
        self.parser.add_argument(
            '-c', '--clean', action="store_true",
            help='clean output'
        )
        self.parser.add_argument(
            '-si', '--show-input', action="store_true",
            help="get input model names"
        )
        self.parser.add_argument(
            '-so', '--show-output', action="store_true",
            help="get output model names"
        )
        self.parser.add_argument(
            '-do', '--desired-output', action="store_true",
            help="get the output of the desired model names"
        )
        self.parser.add_argument(
            '-r', '--run', action="store_true",
            help="copy input skins to output dir"
        )
        self.parser.add_argument(
            '-tf', '--textfile', help="Model names output"
        )
        self.parser.add_argument(
            '-id', '--input-dir',
            help='Input directory'
        )
        self.parser.add_argument(
            '-od', '--output-dir',
            help='Output directory'
        )

    def run(self):
        # Chamba
        args = self.parser.parse_args()

        if isinstance(args.textfile, str):
            self.model_service.set_textfile_of_names( args.textfile )
        if isinstance(args.input_dir, str):
            self.model_service.set_input_dir( args.input_dir )
        if isinstance(args.output_dir, str):
            self.model_service.set_output_dir( args.output_dir )


        ## Mostrar input o output
        if args.show_input:
            dict_input_models = self.model_service.get_dict_input_models()
            model_names = self.model_service.get_input_model_names( dict_input_models )
            list_to_string = '\n'.join( name for name in model_names)
            print(
                f"input models:\n"
                f"---\n"
                f"{list_to_string}\n"
                f"---\n"
                f"models: {len(model_names)}"
            )
        if args.show_output:
            dict_output_models = self.model_service.get_dict_output_models()
            model_names = self.model_service.get_output_model_names( dict_output_models )
            list_to_string = '\n'.join( name for name in model_names)
            print(
                f"output models:\n"
                f"---\n"
                f"{list_to_string}\n"
                f"---\n"
                f"models: {len(model_names)}"
            )
        if args.desired_output:
            model_names = self.model_service.get_model_names_of_textfile()
            list_to_string = '\n'.join( name for name in model_names)
            print(
                f"desired output models:\n"
                f"---\n"
                f"{list_to_string}\n"
                f"---\n"
                f"models: {len(model_names)}"
            )

        ## Limpiar output, o copiar input a output
        if args.clean:
            if self.model_service.clean_output():
                print( "cleaned" )
        if args.run:
            # A copiar archivos
            dict_input_models = self.model_service.get_dict_input_models()

            if not (args.mode in DICT_COPY_MODES.keys()):
                mode = "normal"
            else:
                mode = args.mode
            self.model_service.input_to_output_models( dict_input_models, mode=mode )

