# Third-party imports
from pydantic_settings import BaseSettings


# Project imports
from ._version import __version__
from . import api

# Parameters
# TODO: Move these into a settings.json?
CHECK_DATASETS = True  # Check datasets are sensible before uploading
DEFAULT_TRAIN_TEST_RATIO = 1.0  # Default fraction of data to use for training
PARAMS_COERCION = {  # Convert parameter names in params dict
    "test_train_ratio": "train_test_ratio",  # Common mistake
    "filename": "dataset_id",  # Support old name
    "filename_std": "dataset_std_id",  # Support old name
    "filename_stdv": "dataset_std_id",
    "filename_stdev": "dataset_std_id",
    "dataset": "dataset_id",  # Support old name
    "dataset_std": "dataset_std_id",  # Support old name
    "dataset_stdv": "dataset_std_id",
    "dataset_stdev": "dataset_std_id",
    "functional_input": "decompose_inputs",
    "functional_output": "decompose_outputs",
    "function_input": "decompose_inputs",
    "function_output": "decompose_outputs",
}


class Environment(BaseSettings):
    TWINLAB_URL: str
    TWINLAB_API_KEY: str

    class ConfigDict:
        env_prefix = ""
        case_sensitive = False
        env_file = "./../../.env"
        env_file_encoding = "utf-8"
        extra = "ignore"


ENV = Environment()

user_info = api.get_user()
twinlab_user = user_info["username"]
twinlab_credits = user_info["credits"]

print()
print("         === TwinLab Client Initialisation ===")
print(f"         Version  : {__version__}")
print(f"         User     : {twinlab_user}")
print(f"         Credits  : {twinlab_credits}")
print(f"         Server   : {ENV.TWINLAB_URL}")
print(f"         Key      : {ENV.TWINLAB_API_KEY}")
print()
