
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app.models import db, Equipo, Mantenimiento

main = Blueprint('main', __name__)


@main.route('/')
def inicio():
    from datetime import date

    total_equipos = Equipo.query.count()

    total_mantenimientos = Mantenimiento.query.count()

    pendientes = Mantenimiento.query.filter_by(
        estado='Pendiente'
    ).count()

    completados = Mantenimiento.query.filter_by(
        estado='Completado'
    ).count()

    vencidos = Mantenimiento.query.filter(
        Mantenimiento.estado == 'Pendiente',
        Mantenimiento.fecha_programada < date.today()
    ).count()

    return render_template(
        'index.html',
        total_equipos=total_equipos,
        total_mantenimientos=total_mantenimientos,
        pendientes=pendientes,
        completados=completados,
        vencidos=vencidos
    )


@main.route('/equipos', methods=['GET', 'POST'])
def equipos():

    if request.method == 'POST':
        codigo = request.form.get('codigo', '').strip().upper()
        nombre = request.form.get('nombre', '').strip()
        area = request.form.get('area', '').strip()
        fecha = request.form.get('fecha_ultimo_mantenimiento', '')

        if not all([codigo, nombre, area, fecha]):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('main.equipos'))

        try:
            fecha_convertida = datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            flash('La fecha ingresada no es válida.', 'error')
            return redirect(url_for('main.equipos'))

        equipo = Equipo(
            codigo=codigo,
            nombre=nombre,
            area=area,
            fecha_ultimo_mantenimiento=fecha_convertida
        )

        db.session.add(equipo)

        try:
            db.session.commit()
            flash('Equipo registrado correctamente.', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Ya existe un equipo con ese código.', 'error')

        return redirect(url_for('main.equipos'))

    lista_equipos = Equipo.query.order_by(Equipo.codigo).all()

    return render_template(
        'equipos.html',
        equipos=lista_equipos
    )

@main.route('/mantenimientos', methods=['GET', 'POST'])
def mantenimientos():

    if request.method == 'POST':
        equipo_id = request.form.get('equipo_id', type=int)
        fecha = request.form.get('fecha_programada', '')
        descripcion = request.form.get('descripcion', '').strip()

        if not equipo_id or not fecha or not descripcion:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('main.mantenimientos'))

        equipo = db.session.get(Equipo, equipo_id)

        if equipo is None:
            flash('El equipo seleccionado no existe.', 'error')
            return redirect(url_for('main.mantenimientos'))

        try:
            fecha_convertida = datetime.strptime(
                fecha, '%Y-%m-%d'
            ).date()
        except ValueError:
            flash('La fecha ingresada no es válida.', 'error')
            return redirect(url_for('main.mantenimientos'))

        mantenimiento = Mantenimiento(
            equipo_id=equipo_id,
            fecha_programada=fecha_convertida,
            descripcion=descripcion,
            estado='Pendiente'
        )

        db.session.add(mantenimiento)
        db.session.commit()

        flash('Mantenimiento programado correctamente.', 'success')
        return redirect(url_for('main.mantenimientos'))

    lista_equipos = Equipo.query.order_by(Equipo.codigo).all()

    lista_mantenimientos = Mantenimiento.query.order_by(
        Mantenimiento.fecha_programada
    ).all()

    return render_template(
        'mantenimientos.html',
        equipos=lista_equipos,
        mantenimientos=lista_mantenimientos
    )


@main.route('/mantenimientos/<int:id>/completar', methods=['POST'])
def completar_mantenimiento(id):

    mantenimiento = db.session.get(Mantenimiento, id)

    if mantenimiento is None:
        flash('El mantenimiento solicitado no existe.', 'error')
        return redirect(url_for('main.mantenimientos'))

    mantenimiento.estado = 'Completado'
    db.session.commit()

    flash('Mantenimiento marcado como completado.', 'success')

    return redirect(url_for('main.mantenimientos'))
