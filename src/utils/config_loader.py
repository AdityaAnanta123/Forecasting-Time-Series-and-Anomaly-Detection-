import os
import yaml
from dotenv import load_dotenv

class Config:
    #Take a configuration from YAML File and .env

    def __init__(self, config_path: str = None):
        # Setup Path File Configuration
        if config_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(current_dir, "../../"))
            config_path = os.path.join(project_root, "config", "config.yaml")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"❌ Config file not found: {config_path}")

        # Load Environment
        load_dotenv()

        # Load YAML config
        with open(config_path, "r") as file:
            self._config = yaml.safe_load(file) or {}

    def get(self, *keys, default=None):
        #Acces nested key from config file
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
        return value if value is not None else default

    @property
    def database_url(self) -> str:
        #Generate SQLAlchemy connection string.
        
        user = os.getenv("POSTGRES_USER", self.get("database", "user"))
        password = os.getenv("POSTGRES_PASSWORD", self.get("database", "password"))
        host = os.getenv("POSTGRES_HOST", self.get("database", "host"))
        port = os.getenv("POSTGRES_PORT", str(self.get("database", "port", 5432)))
        db = os.getenv("POSTGRES_DB", self.get("database", "db_name"))

        if not all([user, password, host, db]):
            raise ValueError("⚠️ Incomplete database configuration detected.")

        return f"postgresql://{user}:{password}@{host}:{port}/{db}"
