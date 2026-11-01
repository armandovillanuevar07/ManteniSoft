
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Equipo(db.Model):
    __tablename__ = "equipos"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    fecha_ultimo_mantenimiento = db.Column(db.Date, nullable=False)

    mantenimientos = db.relationship(
        "Mantenimiento",
        backref="equipo",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Equipo {self.codigo}: {self.nombre}>"


class Mantenimiento(db.Model):
    __tablename__ = "mantenimientos"

    id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(
        db.Integer,
        db.ForeignKey("equipos.id"),
        nullable=False
    )
    fecha_programada = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.String(250), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default="Pendiente")

    def __repr__(self):
        return f"<Mantenimiento {self.id}: {self.estado}>"
