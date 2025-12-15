import random
import shutil
from utils import ResourceLoader
from core.text_util import read_text, ignore_comment
from pathlib import Path


# Rutas
resource_loader = ResourceLoader()

INPUT_DIR = resource_loader.get_base_path("input")
OUTPUT_DIR = resource_loader.get_base_path("output")

SKIN_MODELS_TEXTFILE = resource_loader.get_base_path( "skin_models.txt" )

TEXTURE_EXTENSION = ".txd"
MODEL_EXTENSION = ".dff"


# Funciones
def get_skins_of_textfile():
    # Leer texto
    normal_text = read_text( SKIN_MODELS_TEXTFILE, option="ModeText" )
    text_ready = ignore_comment( normal_text, comment="#" )

    # Lista de skins
    skins = []
    for text in text_ready.split("\n"):
        if text == "":
            continue
        else:
            skins.append( text )
    return skins





def get_dict_of_correct_skins_in_dir( path ):
    '''
    Obtener diccionario con archivos en un directorio, con deterinasin si es skin o no.

    Obtener nombres de skins, solo archivos que tengan `.dff` y `txt`, llamados de la misma manera.
    '''
    # Preparar diccionario para validacion de skins
    dict_path = resource_loader.get_recursive_tree( path )
    dict_correct_skins = {}
    for skin_file in dict_path['file']:
        name = skin_file.name
        skin_model_name = name[:-4]

        dict_correct_skins.update({
            skin_model_name: {
                "is_a_skin": False,
                "filetxd": None,
                "filedff": None
            }
        })

    # Paso dos, determinar que sea skin
    for skin_file in dict_path['file']:
        # Si el nombre tiene como ultimas cuatro letras ".dff" o ".txd", esta bien.
        name = skin_file.name
        skin_model_name = name[:-4]
        file_extension = name[-4:]
        is_dff = file_extension == MODEL_EXTENSION
        is_txd = file_extension == TEXTURE_EXTENSION
        if is_dff:
            dict_correct_skins[skin_model_name]["filedff"] = skin_file
        elif is_txd:
            dict_correct_skins[skin_model_name]["filetxd"] = skin_file

        # Validado skin
        dict_correct_skins[skin_model_name]["is_a_skin"] = (
            (not dict_correct_skins[skin_model_name]["filedff"] == None) and
            (not dict_correct_skins[skin_model_name]["filetxd"] == None)
        )

    return dict_correct_skins


def get_dict_input_skins():
    return get_dict_of_correct_skins_in_dir( INPUT_DIR )


def get_dict_output_skins():
    return get_dict_of_correct_skins_in_dir( OUTPUT_DIR )


def get_name_of_correct_skins( dict_correct_skins ):
    name_of_skins = []
    for name in dict_correct_skins.keys():
        dict_skin = dict_correct_skins[name]
        if dict_skin["is_a_skin"]:
            name_of_skins.append( name )
    return name_of_skins


def get_output_skin_model_names( ):
    return get_name_of_correct_skins( get_dict_output_skins() )


def get_input_skin_model_names( dict_input_skins={} ):
    return get_name_of_correct_skins( get_dict_input_skins() )


def input_to_output_skins( dict_input_skins={}, mode="normal" ):
    '''
    Copiar input skins a output
    > Se supone que output, no importa que se le remplaze todo todote.

    Modos
    - normal
    - random
    - random_counted
    '''
    # Obtener skins listos para usar
    name_of_input_skins = get_input_skin_model_names( dict_input_skins=dict_input_skins )
    number_of_input_skins = len( name_of_input_skins )-1

    # Modo de guardado
    skin_model_names = get_skins_of_textfile()
    if number_of_input_skins >= 0:
        if mode == "random":
            pass
        else:
            count = 0
            for model_name in skin_model_names:
                # Skins files
                dict_skin = dict_input_skins[ name_of_input_skins[count] ]
                output_filedff = OUTPUT_DIR.joinpath( f"{model_name}{MODEL_EXTENSION}" )
                output_filetxd = OUTPUT_DIR.joinpath( f"{model_name}{TEXTURE_EXTENSION}" )
                print( dict_skin[ "filedff"], "to", output_filedff )
                print( dict_skin[ "filetxd"], "to", output_filetxd )

                # Copiar
                shutil.copy( dict_skin[ "filedff"], output_filedff )
                shutil.copy( dict_skin[ "filetxd"], output_filetxd )
                if count == number_of_input_skins:
                    count = 0
                else:
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
    '-m', '--mode', help='Set copy mode of input to output'
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
    print( f"Input models: {get_input_skin_model_names()}" )
if args.show_output:
    print( f"Output models: {get_output_skin_model_names()}" )
if args.desired_output:
    print( f"Desired output models: {get_skins_of_textfile()}" )

## Limpiar output, o copair input a output
if args.clean:
    if clean_output():
        print( "Cleaned" )
if args.run:
    # A copiar archivos
    dict_input_skins = get_dict_input_skins()
    input_to_output_skins( dict_input_skins, mode=str(args.mode) )


