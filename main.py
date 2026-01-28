from core.servicies.gta_3d_mapper.model_service import ModelService
from interface.cli.gta_3d_mapper.gta_3d_mapper_cli import GTA3DMapperCLI

from config.paths import INPUT_DIR, OUTPUT_DIR, MODEL_OUTPUT_NAMES_TEXTFILE

model_service = ModelService( INPUT_DIR, OUTPUT_DIR, MODEL_OUTPUT_NAMES_TEXTFILE )
cli = GTA3DMapperCLI( model_service )

if __name__ == '__main__':
    cli.run()
