from flask import (
    Blueprint,
    request,
    jsonify
)

from database import db

from models import (
    AuthorizedUser,
    EventLog
)


access_bp = Blueprint(
    'access',
    __name__
)


@access_bp.route(
    '/register_access',
    methods=['POST']
)
def register_access():

    data = request.get_json()

    rfid_tag = data.get('rfid_tag')

    bin_id = data.get('bin_id')

    user = AuthorizedUser.query.filter_by(
        rfid_tag=rfid_tag,
        active=True
    ).first()

    if not user:

        log = EventLog(
            bin_id=bin_id,
            event_type='ACESSO_NEGADO',
            message='RFID não autorizado'
        )

        db.session.add(log)
        db.session.commit()

        return jsonify({
            'error': 'Acesso negado'
        }), 403

    log = EventLog(
        bin_id=bin_id,
        user_id=user.id,
        event_type='ABERTURA_PARA_DESCARTE',
        message='Tampa liberada'
    )

    db.session.add(log)
    db.session.commit()

    return jsonify({
        'message': 'Tampa aberta'
    })