import random
import shutil
from utils import ResourceLoader
from core.text_util import read_text, ignore_comment, not_repeat_item
from pathlib import Path


# Rutas
resource_loader = ResourceLoader()

INPUT_DIR = resource_loader.get_base_path("input")
OUTPUT_DIR = resource_loader.get_base_path("output")

MODEL_OUTPUT_NAMES_TEXTFILE = resource_loader.get_base_path( "model_output_names.txt" )

TEXTURE_EXTENSION = ".txd"
MODEL_EXTENSION = ".dff"


# Funciones
def get_model_names_of_textfile():
    # Leer texto
    normal_text = read_text( MODEL_OUTPUT_NAMES_TEXTFILE, option="ModeText" )
    text_ready = ignore_comment( normal_text, comment="#" )

    # Lista de skins
    skins = []
    for text in text_ready.split("\n"):
        if text == "":
            continue
        else:
            skins.append( text )
    return not_repeat_item( skins ) # No repetir skins.





def get_dict_of_correct_models_in_dir( path ):
    '''
    Obtener diccionario con archivos en un directorio, con deterinasin si es skin o no.

    Obtener nombres de skins, solo archivos que tengan `.dff` y `txt`, llamados de la misma manera.
    '''
    # Preparar diccionario para validacion de skins
    dict_path = resource_loader.get_recursive_tree( path )
    dict_correct_models = {}
    for model_file in dict_path['file']:
        name = model_file.name
        model_name = name[:-4]

        dict_correct_models.update({
            model_name: {
                "is_a_model": False,
                "filetxd": None,
                "filedff": None
            }
        })

    # Paso dos, determinar que sea skin
    for model_file in dict_path['file']:
        # Si el nombre tiene como ultimas cuatro letras ".dff" o ".txd", esta bien.
        name = model_file.name
        model_name = name[:-4]
        file_extension = name[-4:]
        is_dff = file_extension == MODEL_EXTENSION
        is_txd = file_extension == TEXTURE_EXTENSION
        if is_dff:
            dict_correct_models[model_name]["filedff"] = model_file
        elif is_txd:
            dict_correct_models[model_name]["filetxd"] = model_file

        # Validado skin
        dict_correct_models[model_name]["is_a_model"] = (
            (not dict_correct_models[model_name]["filedff"] == None) and
            (not dict_correct_models[model_name]["filetxd"] == None)
        )

    return dict_correct_models


def get_dict_input_models():
    return get_dict_of_correct_models_in_dir( INPUT_DIR )


def get_dict_output_models():
    return get_dict_of_correct_models_in_dir( OUTPUT_DIR )


def get_name_of_correct_models( dict_correct_models ):
    name_of_models = []
    for name in dict_correct_models.keys():
        dict_model = dict_correct_models[name]
        if dict_model["is_a_model"]:
            name_of_models.append( name )
    return name_of_models


def get_output_model_names( ):
    return get_name_of_correct_models( get_dict_output_models() )


def get_input_model_names( dict_input_models={} ):
    return get_name_of_correct_models( get_dict_input_models() )



DICT_COPY_MODES = {
    "normal": 0, "random_counted": 1, "random": 2
}
def input_to_output_models( dict_input_models={}, mode="normal" ):
    '''
    Copiar input skins a output
    > Se supone que output, no importa que se le remplaze todo todote.

    Modos
    - normal
    - random
    - random_counted
    '''
    # Obtener skins listos para usar
    name_of_input_models = get_input_model_names( dict_input_models=dict_input_models )
    number_of_input_models = len( name_of_input_models )-1

    # Modo de guardado
    model_names = get_model_names_of_textfile()
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
            output_filedff = OUTPUT_DIR.joinpath( f"{model_name}{MODEL_EXTENSION}" )
            output_filetxd = OUTPUT_DIR.joinpath( f"{model_name}{TEXTURE_EXTENSION}" )

            # Copiar
            shutil.copy( dict_model[ "filedff"], output_filedff )
            shutil.copy( dict_model[ "filetxd"], output_filetxd )

            # Debug
            text_prefix = f"Mode `{mode}` | Counter `{count}`"
            print( f'{text_prefix} | {dict_model[ "filedff"]} to {output_filedff}' )
            print( f'{text_prefix} | {dict_model[ "filetxd"]} to {output_filetxd}' )

            # Contar
            if activate_counter:
                count += 1




def clean_folder_dff_txd(folder: Path):
    for item in folder.rglob("*"):
        if item.is_file() and item.suffix.lower() in (".dff", ".txd"):
            item.unlink()


def clean_output():
    good_remove = False
    try:
        clean_folder_dff_txd( OUTPUT_DIR )
        good_remove = True
    finally:
        return good_remove




# Argparse moment
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    '-m', '--mode', help='Set copy mode of input to output. Modes: "normal", "random_counted", "random"'
)
parser.add_argument(
    '-c', '--clean', action="store_true", help='Clean output'
)
parser.add_argument(
    '-si', '--show-input', action="store_true", help="Get input model names"
)
parser.add_argument(
    '-so', '--show-output', action="store_true", help="Get output model names"
)
parser.add_argument(
    '-do', '--desired-output', action="store_true", help="Get the output of the desired model names"
)
parser.add_argument(
    '-r', '--run', action="store_true", help="Copy input skins to output dir"
)

args = parser.parse_args()

# Chamba
## Mostrar input o output
if args.show_input:
    model_names = get_input_model_names()
    print( f"Input models: {model_names} {len(model_names)}" )
if args.show_output:
    model_names = get_output_model_names()
    print( f"Output models: {model_names} {len(model_names)}" )
if args.desired_output:
    model_names = get_model_names_of_textfile()
    print( f"Desired output models: {model_names} {len(model_names)}" )

## Limpiar output, o copiar input a output
if args.clean:
    if clean_output():
        print( "Cleaned" )
if args.run:
    # A copiar archivos
    dict_input_models = get_dict_input_models()

    if not (args.mode in DICT_COPY_MODES.keys()):
        mode = "normal"
    else:
        mode = args.mode
    input_to_output_models( dict_input_models, mode=mode )


