from models.gta_3d_mapper.model_files import ModelFile

from config.constants import MODEL_EXTENSION, TEXTURE_EXTENSION, DICT_COPY_MODES

from core.text_util import read_text, ignore_comment, not_repeat_item
from utils import ResourceLoader
import pathlib
import random
import shutil

class ModelService:
    def __init__(
        self, input_dir: pathlib.Path, output_dir: pathlib.Path, textfile_of_names: pathlib.Path
    ):
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.textfile_of_names = textfile_of_names

        self.resource_loader = ResourceLoader()

    def get_model_names_of_textfile(self):
        # Leer texto
        normal_text = read_text( self.textfile_of_names, option="ModeText" )
        text_ready = ignore_comment( normal_text, comment="#" )

        # Lista de skins
        skins = []
        for text in text_ready.split("\n"):
            if text == "":
                continue
            else:
                skins.append( text )
        return not_repeat_item( skins ) # No repetir skins.


    def get_dict_of_correct_models_in_dir( self, path ):
        '''
        Obtener diccionario con archivos en un directorio, con deterina si es skin o no.

        Obtener nombres de skins, solo archivos que tengan `.dff` y `txt`, llamados de la misma manera.
        '''
        # Preparar diccionario para validacion de skins
        dict_path = self.resource_loader.get_recursive_tree( path )
        dict_correct_models = {}
        for f in dict_path['file']:
            name = f.name
            model_file = ModelFile()
            model_file.filetxd = None
            model_file.filedff = None
            model_file.is_a_model = False
            dict_correct_models.update( {name[:-4]: model_file} )

        # Paso dos, determinar que sea skin
        for f in dict_path['file']:
            # Si el nombre tiene como ultimas cuatro letras ".dff" o ".txd", esta bien.
            name = f.name
            model_name = name[:-4]
            file_extension = name[-4:]
            is_dff = file_extension == MODEL_EXTENSION
            is_txd = file_extension == TEXTURE_EXTENSION
            if is_dff:
                dict_correct_models[model_name].filedff = f
            elif is_txd:
                dict_correct_models[model_name].filetxd = f

            # Validado skin
            dict_correct_models[model_name].is_a_model = (
                (not dict_correct_models[model_name].filedff == None) and
                (not dict_correct_models[model_name].filetxd == None)
            )

        return dict_correct_models

    def get_dict_input_models(self):
        return self.get_dict_of_correct_models_in_dir( self.input_dir )

    def get_dict_output_models(self):
        return self.get_dict_of_correct_models_in_dir( self.output_dir )

    def get_name_of_correct_models( self, dict_correct_models ):
        name_of_models = []
        for name in dict_correct_models.keys():
            dict_model = dict_correct_models[name]
            if dict_model.is_a_model:
                name_of_models.append( name )
        return name_of_models

    def get_output_model_names( self, dict_output_models={} ):
        return self.get_name_of_correct_models( dict_output_models )

    def get_input_model_names( self, dict_input_models={} ):
        return self.get_name_of_correct_models( dict_input_models )

    def input_to_output_models( self, dict_input_models, mode="normal" ):
        '''
        Copiar input skins a output
        > Se supone que output, no importa que se le remplaze todo todote.

        Modos
        - normal
        - random
        - random_counted
        '''
        # Obtener skins listos para usar
        name_of_input_models = self.get_input_model_names( dict_input_models )
        number_of_input_models = len( name_of_input_models )-1

        # Modo de guardado
        model_names = self.get_model_names_of_textfile()
        if number_of_input_models >= 0 and (mode in DICT_COPY_MODES.keys()):
            mode_number = DICT_COPY_MODES[mode]
            count = 0
            deletable_name_of_input_models = list(name_of_input_models)
            activate_counter = mode_number != DICT_COPY_MODES["random"]
            for model_name in model_names:
                # Recomodar contador
                if count > number_of_input_models:
                    count = 0
                    deletable_name_of_input_models = list(name_of_input_models)

                # Modo
                selected_key = name_of_input_models[count] # 'normal' mode
                if mode_number == DICT_COPY_MODES["random"]:
                    selected_key = random.choice( name_of_input_models )
                    activate_counter = False
                elif mode_number == DICT_COPY_MODES["random_counted"]:
                    # Elegir en lista borrable, de forma aleleatorio, y elimminar de la lista opcion seleccionada.
                    selected_index = random.randint(0, len(deletable_name_of_input_models)-1 )
                    selected_key = deletable_name_of_input_models[selected_index]
                    del deletable_name_of_input_models[selected_index]

                ## Skin seleccionada
                dict_model = dict_input_models[ selected_key ]

                # Files
                output_filedff = self.output_dir.joinpath( f"{model_name}{MODEL_EXTENSION}" )
                output_filetxd = self.output_dir.joinpath( f"{model_name}{TEXTURE_EXTENSION}" )

                # Copiar
                shutil.copy( dict_model.filedff, output_filedff )
                shutil.copy( dict_model.filetxd, output_filetxd )

                # Debug
                text_prefix = f"Mode `{mode}` | Counter `{count}`"
                print( f'{text_prefix} | {dict_model.filedff} to {output_filedff}' )
                print( f'{text_prefix} | {dict_model.filetxd} to {output_filetxd}' )

                # Contar
                if activate_counter:
                    count += 1

    def clean_folder_dff_txd(self, folder: pathlib.Path):
        for item in folder.rglob("*"):
            print(item)
            if item.is_file() and item.suffix.lower() in (MODEL_EXTENSION, TEXTURE_EXTENSION):
                item.unlink()

    def clean_output(self):
        good_remove = False
        try:
            self.clean_folder_dff_txd( self.output_dir )
            good_remove = True
        finally:
            return good_remove
