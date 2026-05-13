import pandas as pd

from flask import (
    Blueprint,
    jsonify,
    send_file
)

from models import (
    SmartBin,
    EventLog
)


monitoring_bp = Blueprint(
    'monitoring',
    __name__
)


@monitoring_bp.route(
    '/monitoring',
    methods=['GET']
)
def monitoring():

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


@monitoring_bp.route(
    '/logs',
    methods=['GET']
)
def logs():

    logs = EventLog.query.all()

    result = []

    for log in logs:

        result.append({
            'bin_id': log.bin_id,
            'user_id': log.user_id,
            'event_type': log.event_type,
            'level': log.level,
            'message': log.message,
            'timestamp': log.timestamp
        })

    return jsonify(result)


@monitoring_bp.route(
    '/export/logs',
    methods=['GET']
)
def export_logs():

    logs = EventLog.query.all()

    data = []

    for log in logs:

        data.append({
            'bin_ID': log.bin_id,
            'user_ID': log.user_id,
            'event_type': log.event_type,
            'level': log.level,
            'message': log.message,
            'timestamp': log.timestamp
        })

    df = pd.DataFrame(data)

    file_path = 'exports/logs.csv'

    df.to_csv(
        file_path,
        index=False
    )

    return send_file(
        file_path,
        as_attachment=True
    )