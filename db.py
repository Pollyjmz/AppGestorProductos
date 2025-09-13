from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Base para modelos
Base = declarative_base()

# Modelo Producto
class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

# Conexión a la base SQLite (archivo productos.db)
engine = create_engine("sqlite:///database\productos.db", echo=True)

# Crear tablas si no existen
Base.metadata.create_all(engine)

# Crear sesión
Session = sessionmaker(bind=engine)
