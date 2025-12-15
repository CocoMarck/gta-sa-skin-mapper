import random
import shutil
from utils import ResourceLoader
from core.text_util import read_text, ignore_comment


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


def get_dict_input_skins():
    '''
    Obtener nombres de skins, solo archivos que tengan `.dff` y `txt`, lamados de la misma manera.
    '''
    dict_input_dir = resource_loader.get_recursive_tree( INPUT_DIR )

    # Preparar diccionario para validacion de skins
    dict_correct_skins = {}
    for skin_file in dict_input_dir['file']:
        name = skin_file.name
        skin_model_name = name[:-4]
        if skin_model_name in dict_input_dir.keys():
            continue
        dict_correct_skins.update({
            skin_model_name: {
                "is_a_skin": False,
                "filetxd": None,
                "filedff": None
            }
        })

    # Agregando skin
    for skin_file in dict_input_dir['file']:
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
    name_of_input_skins = []
    for name in dict_input_skins.keys():
        dict_skin = dict_input_skins[name]
        if dict_skin["is_a_skin"]:
            name_of_input_skins.append( name )
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




# Rutas de skins en input
skin_model_names = get_skins_of_textfile()
dict_input_skins = get_dict_input_skins()

# Debug
#print(skin_model_names)
input_to_output_skins( dict_input_skins )
