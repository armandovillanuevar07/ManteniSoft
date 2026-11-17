import pytest
from app import create_app
from app.models import db, Equipo, Mantenimiento
from datetime import date, timedelta

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
        db.engine.dispose()

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

def crear_mantenimientos_seguimiento(app):
    with app.app_context():
        equipo = Equipo.query.filter_by(codigo='EQ-001').first()

        if equipo is None:
            equipo = Equipo(
                codigo='EQ-001',
                nombre='Bomba principal',
                area='Planta',
                fecha_ultimo_mantenimiento=date(2026, 10, 15)
            )
            db.session.add(equipo)
            db.session.commit()

        hoy = date.today()

        registros = [
            Mantenimiento(
                equipo_id=equipo.id,
                fecha_programada=hoy - timedelta(days=10),
                descripcion='Mantenimiento vencido 1',
                estado='Pendiente'
            ),
            Mantenimiento(
                equipo_id=equipo.id,
                fecha_programada=hoy - timedelta(days=5),
                descripcion='Mantenimiento vencido 2',
                estado='Pendiente'
            ),
            Mantenimiento(
                equipo_id=equipo.id,
                fecha_programada=hoy + timedelta(days=10),
                descripcion='Mantenimiento pendiente',
                estado='Pendiente'
            ),
            Mantenimiento(
                equipo_id=equipo.id,
                fecha_programada=hoy + timedelta(days=15),
                descripcion='Mantenimiento completado',
                estado='Completado'
            )
        ]

        db.session.add_all(registros)
        db.session.commit()

def test_seguimiento_muestra_todos(client, app):
    crear_mantenimientos_seguimiento(app)

    respuesta = client.get('/seguimiento?estado=Todos')

    assert respuesta.status_code == 200
    assert b'Mantenimiento vencido 1' in respuesta.data
    assert b'Mantenimiento vencido 2' in respuesta.data
    assert b'Mantenimiento pendiente' in respuesta.data
    assert b'Mantenimiento completado' in respuesta.data

def test_seguimiento_filtra_pendientes(client, app):
    crear_mantenimientos_seguimiento(app)

    respuesta = client.get('/seguimiento?estado=Pendiente')

    assert respuesta.status_code == 200
    assert b'Mantenimiento pendiente' in respuesta.data
    assert b'Mantenimiento vencido 1' not in respuesta.data
    assert b'Mantenimiento vencido 2' not in respuesta.data
    assert b'Mantenimiento completado' not in respuesta.data

def test_seguimiento_filtra_vencidos(client, app):
    crear_mantenimientos_seguimiento(app)

    respuesta = client.get('/seguimiento?estado=Vencido')

    assert respuesta.status_code == 200
    assert b'Mantenimiento vencido 1' in respuesta.data
    assert b'Mantenimiento vencido 2' in respuesta.data
    assert b'Mantenimiento pendiente' not in respuesta.data
    assert b'Mantenimiento completado' not in respuesta.data

def test_seguimiento_filtra_completados(client, app):
    crear_mantenimientos_seguimiento(app)

    respuesta = client.get('/seguimiento?estado=Completado')

    assert respuesta.status_code == 200
    assert b'Mantenimiento completado' in respuesta.data
    assert b'Mantenimiento vencido 1' not in respuesta.data
    assert b'Mantenimiento vencido 2' not in respuesta.data
    assert b'Mantenimiento pendiente' not in respuesta.data

def test_registrar_equipo_campos_vacios(client):
    respuesta = client.post('/equipos', data={
        'codigo': '',
        'nombre': 'Bomba principal',
        'area': 'Planta',
        'fecha_ultimo_mantenimiento': '2026-10-15'
    }, follow_redirects=True)

    assert respuesta.status_code == 200
    assert b'Todos los campos son obligatorios.' in respuesta.data

def test_registrar_equipo_fecha_invalida(client):
    respuesta = client.post('/equipos', data={
        'codigo': 'EQ-002',
        'nombre': 'Compresor',
        'area': 'Planta',
        'fecha_ultimo_mantenimiento': 'fecha-invalida'
    }, follow_redirects=True)

    assert respuesta.status_code == 200
    assert 'La fecha ingresada no es válida.'.encode('utf-8') in respuesta.data

def test_registrar_equipo_codigo_duplicado(client):
    registrar_equipo(client)

    respuesta = client.post('/equipos', data={
        'codigo': 'EQ-001',
        'nombre': 'Bomba secundaria',
        'area': 'Planta',
        'fecha_ultimo_mantenimiento': '2026-10-20'
    }, follow_redirects=True)

    assert respuesta.status_code == 200
    assert 'Ya existe un equipo con ese código.'.encode('utf-8') in respuesta.data

def test_registrar_equipo_metodo_get(client):
    respuesta = client.get('/equipos')

    assert respuesta.status_code == 200
    assert b'EQ-001' not in respuesta.data

def test_programar_mantenimiento_campos_vacios(client):
    respuesta = client.post('/mantenimientos', data={
        'equipo_id': '',
        'fecha_programada': '',
        'descripcion': ''
    }, follow_redirects=True)

    assert respuesta.status_code == 200
    assert 'Todos los campos son obligatorios.'.encode('utf-8') in respuesta.data

def test_programar_mantenimiento_equipo_inexistente(client):
    respuesta = client.post('/mantenimientos', data={
        'equipo_id': '999',
        'fecha_programada': '2026-12-15',
        'descripcion': 'Inspección preventiva'
    }, follow_redirects=True)

    assert respuesta.status_code == 200
    assert 'El equipo seleccionado no existe.'.encode('utf-8') in respuesta.data

def test_programar_mantenimiento_fecha_invalida(client, app):
    registrar_equipo(client)

    with app.app_context():
        equipo = Equipo.query.filter_by(codigo='EQ-001').first()
        equipo_id = equipo.id

    respuesta = client.post('/mantenimientos', data={
        'equipo_id': equipo_id,
        'fecha_programada': 'fecha-invalida',
        'descripcion': 'Inspección preventiva'
    }, follow_redirects=True)

    assert respuesta.status_code == 200
    assert 'La fecha ingresada no es válida.'.encode('utf-8') in respuesta.data

def test_listar_mantenimientos_get(client):
    respuesta = client.get('/mantenimientos')

    assert respuesta.status_code == 200
    assert b'Mantenimientos' in respuesta.data

def test_completar_mantenimiento_inexistente(client):
    respuesta = client.post(
        '/mantenimientos/999/completar',
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert 'El mantenimiento solicitado no existe.'.encode('utf-8') in respuesta.data

def test_seguimiento_filtro_no_reconocido(client, app):
    crear_mantenimientos_seguimiento(app)

    respuesta = client.get('/seguimiento?estado=Desconocido')

    assert respuesta.status_code == 200
    assert b'Mantenimiento vencido 1' in respuesta.data
    assert b'Mantenimiento pendiente' in respuesta.data
    assert b'Mantenimiento completado' in respuesta.data

def test_configuracion_testing(monkeypatch):
    monkeypatch.setenv('FLASK_ENVIRONMENT', 'testing')

    app = create_app({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    try:
        assert app.config['TESTING'] is True
    finally:
        with app.app_context():
            db.session.remove()
            db.engine.dispose()

def test_configuracion_produccion(monkeypatch):
    monkeypatch.setenv('FLASK_ENVIRONMENT', 'production')

    app = create_app({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    try:
        assert app.config['DEBUG'] is False
        assert app.config['TESTING'] is False
    finally:
        with app.app_context():
            db.session.remove()
            db.engine.dispose()

def test_representacion_equipo(client):
    equipo = Equipo(
        codigo='EQ-TEST',
        nombre='Bomba de prueba',
        area='Producción',
        fecha_ultimo_mantenimiento=date.today()
    )

    resultado = repr(equipo)

    assert resultado == '<Equipo EQ-TEST: Bomba de prueba>'

def test_representacion_mantenimiento():
    mantenimiento = Mantenimiento(
        id=1,
        estado='Pendiente'
    )

    resultado = repr(mantenimiento)

    assert resultado == '<Mantenimiento 1: Pendiente>'