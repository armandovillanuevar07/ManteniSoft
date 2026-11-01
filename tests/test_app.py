import pytest
from app import create_app
from app.models import db, Equipo, Mantenimiento


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'clave-pruebas'
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def registrar_equipo(client):
    return client.post('/equipos', data={
        'codigo': 'EQ-001',
        'nombre': 'Bomba principal',
        'area': 'Planta',
        'fecha_ultimo_mantenimiento': '2026-10-15'
    }, follow_redirects=True)


def test_pagina_principal(client):
    respuesta = client.get('/')

    assert respuesta.status_code == 200
    assert b'Panel de seguimiento' in respuesta.data


def test_registrar_equipo(client):
    respuesta = registrar_equipo(client)

    assert respuesta.status_code == 200
    assert b'EQ-001' in respuesta.data


def test_programar_mantenimiento(client, app):
    registrar_equipo(client)

    with app.app_context():
        equipo = Equipo.query.filter_by(codigo='EQ-001').first()
        equipo_id = equipo.id

    respuesta = client.post('/mantenimientos', data={
        'equipo_id': equipo_id,
        'fecha_programada': '2026-11-15',
        'descripcion': 'Inspeccion preventiva'
    }, follow_redirects=True)

    assert respuesta.status_code == 200
    assert b'Inspeccion preventiva' in respuesta.data


def test_completar_mantenimiento(client, app):
    registrar_equipo(client)

    with app.app_context():
        equipo = Equipo.query.filter_by(codigo='EQ-001').first()

        mantenimiento = Mantenimiento(
            equipo_id=equipo.id,
            fecha_programada=__import__('datetime').date(2026, 11, 15),
            descripcion='Cambio de filtros',
            estado='Pendiente'
        )

        db.session.add(mantenimiento)
        db.session.commit()
        mantenimiento_id = mantenimiento.id

    respuesta = client.post(
        f'/mantenimientos/{mantenimiento_id}/completar',
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert b'Completado' in respuesta.data


def test_indicadores_del_panel(client, app):
    registrar_equipo(client)

    with app.app_context():
        equipo = Equipo.query.filter_by(codigo='EQ-001').first()

        mantenimiento = Mantenimiento(
            equipo_id=equipo.id,
            fecha_programada=__import__('datetime').date(2026, 10, 15),
            descripcion='Mantenimiento vencido',
            estado='Pendiente'
        )

        db.session.add(mantenimiento)
        db.session.commit()

    respuesta = client.get('/')

    assert respuesta.status_code == 200
    assert b'Equipos registrados' in respuesta.data