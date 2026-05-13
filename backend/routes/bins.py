from flask import (
    Blueprint,
    request,
    jsonify
)

from database import db

from models import (
    SmartBin,
    EventLog
)

from services.ai_mock import (
    analyze_fill_level
)

from services.level_service import (
    calculate_fill_percentage
)


bins_bp = Blueprint(
    'bins',
    __name__
)


# CREATE
@bins_bp.route(
    '/bins',
    methods=['POST']
)
def create_bin():

    data = request.get_json()

    smart_bin = SmartBin(
        location=data.get('location'),
        current_level=0,
        status='Disponível'
    )

    db.session.add(smart_bin)
    db.session.commit()

    return jsonify({
        'message': 'Lixeira criada'
    })


# READ
@bins_bp.route(
    '/bins',
    methods=['GET']
)
def get_bins():

    bins = SmartBin.query.all()

    result = []

    for b in bins:

        result.append({
            'id': b.id,
            'location': b.location,
            'current_level': b.current_level,
            'status': b.status
        })

    return jsonify(result)


# UPDATE
@bins_bp.route(
    '/bins/<int:id>',
    methods=['PUT']
)
def update_bin(id):

    data = request.get_json()

    smart_bin = SmartBin.query.get(id)

    if not smart_bin:

        return jsonify({
            'error': 'Lixeira não encontrada'
        }), 404

    smart_bin.location = data.get(
        'location',
        smart_bin.location
    )

    smart_bin.status = data.get(
        'status',
        smart_bin.status
    )

    db.session.commit()

    return jsonify({
        'message': 'Lixeira atualizada'
    })


# DELETE
@bins_bp.route(
    '/bins/<int:id>',
    methods=['DELETE']
)
def delete_bin(id):

    smart_bin = SmartBin.query.get(id)

    if not smart_bin:

        return jsonify({
            'error': 'Lixeira não encontrada'
        }), 404

    db.session.delete(smart_bin)

    db.session.commit()

    return jsonify({
        'message': 'Lixeira deletada'
    })


# UPDATE LEVEL
@bins_bp.route(
    '/update_level/<int:id>',
    methods=['POST']
)
def update_level(id):

    data = request.get_json()

    distance = data.get('distance')

    smart_bin = SmartBin.query.get(id)

    if not smart_bin:

        return jsonify({
            'error': 'Lixeira não encontrada'
        }), 404

    level = calculate_fill_percentage(
        distance
    )

    smart_bin.current_level = level

    alert = analyze_fill_level(level)

    smart_bin.status = alert

    log = EventLog(
        bin_id=id,
        event_type='NIVEL_ATUALIZADO',
        level=level,
        message=alert
    )

    db.session.add(log)

    if level >= 90:

        full_log = EventLog(
            bin_id=id,
            event_type='LIXEIRA_CHEIA',
            level=level,
            message='Lixeira atingiu 90%'
        )

        db.session.add(full_log)

    db.session.commit()

    return jsonify({
        'level': level,
        'alert': alert
    })