import warnings
from google.cloud.firestore_v1.base_collection import UserWarning

warnings.filterwarnings("ignore", category=UserWarning)
