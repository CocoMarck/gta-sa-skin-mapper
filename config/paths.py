from utils import ResourceLoader

resource_loader = ResourceLoader()

# Rutas
INPUT_DIR = resource_loader.get_base_path("input")
OUTPUT_DIR = resource_loader.get_base_path("output")

MODEL_OUTPUT_NAMES_TEXTFILE = resource_loader.get_base_path( "model_output_names.txt" )
