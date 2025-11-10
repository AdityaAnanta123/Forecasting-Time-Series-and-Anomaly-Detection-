import logging
import logging.config
import yaml
import os

def setup_logger(name: str = "app", config_path: str = None):
    """
    Initialize logger from YAML config file.
    Jika logging.yaml tidak ditemukan → fallback ke basicConfig.
    """
    if config_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "../../"))
        config_path = os.path.join(project_root, "config", "logging.yaml")

    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            log_cfg = yaml.safe_load(file)

        # 🟢 Pastikan direktori log ada
        for handler in log_cfg.get("handlers", {}).values():
            if "filename" in handler:
                log_path = handler["filename"]
                log_dir = os.path.dirname(log_path)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir, exist_ok=True)
                    print(f"📁 Created log directory: {log_dir}")

        logging.config.dictConfig(log_cfg)
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        print(f"⚠️ Logging config not found at {config_path}, using basic logger.")

    logger = logging.getLogger(name)
    logger.info("✅ Logger initialized successfully.")
    return logger
