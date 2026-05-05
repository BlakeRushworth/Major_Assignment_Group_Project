from pathlib import Path


class AppConfig:
    

    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    DATESET_DIR = RAW_DATA_DIR / "stream_macroinvertebrates"
    OUTPUTS_DIR = BASE_DIR / "outputs"
    EDA_OUTPUT_DIR = OUTPUTS_DIR / "eda"
    MODEL_OUTPUT_DIR = OUTPUTS_DIR / "models"
    IMAGE_SIZE = (128, 128)
    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}

    
    
    @classmethod
    def create_required_dir(cls):
        for path in [cls.DATA_DIR,
                    cls.RAW_DATA_DIR,
                    cls.OUTPUTS_DIR,
                    cls.EDA_OUTPUT_DIR,
                    cls.MODEL_OUTPUT_DIR]:
            path.mkdir(parents = True, exist_ok = True)