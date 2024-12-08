from flask import Blueprint, request, jsonify
from app.kafka_service import KafkaService
from werkzeug.exceptions import BadRequest

queue_bp = Blueprint('queue', __name__)

@queue_bp.route('/set_data', methods=['POST'])
def set_data():
    """
    Роут для записи данных в Kafka
    """
    try:
        data = request.get_json()
        receiver_id = data.get('receiver_id')
        sender_id = data.get('sender_id')
        message_data = data.get('data')

        if not receiver_id or not sender_id or not message_data:
            raise BadRequest("Missing required fields: 'receiver_id', 'sender_id', or 'data'.")

        KafkaService.send_message(receiver_id, sender_id, message_data)

        return jsonify({"message": "Data successfully sent to the queue."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@queue_bp.route('/get_data', methods=['GET'])
def get_data():
    """
    Роут для получения последних данных из Kafka
    """
    try:
        receiver_id = request.args.get('receiver_id')
        if not receiver_id:
            raise BadRequest("Missing required parameter: 'receiver_id'.")

        topic = f"asutk_ms_{receiver_id}"


        data = KafkaService.consume_message(receiver_id)

        if data is None:
            return jsonify({"error": "No data found in the queue."}), 404

        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
