from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.config_loader import Config
from utils.logger import setup_logger

logger = setup_logger()
config = Config()

#Setup URL Connection to Database#
DATABASE_URL = config.database_url
logger.info(f"Connecting to database: {DATABASE_URL}")

#SQLAlchemy Engine & Session#
engine = create_engine(DATABASE_URL, pool_pre_ping = True)
SessionLocal = sessionmaker(autocommit = False, autoFlush = False, bind = engine)

#Dependency from FastAPI#
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Test connection to database#
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            logger.info("✅ Database connection successful!")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
