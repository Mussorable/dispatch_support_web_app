from flask import jsonify

from app import db
from app.api import bp
from app.models import Transport


# List of transport with selected type
@bp.route('/<transport_type>', methods=['GET'])
def get_transport(transport_type):
    vehicle_class = Transport.get_transport_type(transport_type)
    vehicle_list = vehicle_class.query.all()
    return jsonify([vehicle.to_dict() for vehicle in vehicle_list])


# Information about specific vehicle
@bp.route('/<transport_type>/<int:id>', methods=["GET"])
def get_transport_specific_vehicle(transport_type, id):
    vehicle_class = Transport.get_transport_type(transport_type)
    return db.get_or_404(vehicle_class, id)


# Lists of all vehicles in system
@bp.route('/vehicles', methods=['GET'])
def get_vehicles():
    truck_list, trailer_list = Transport.get_lists_of_vehicles()
    return jsonify({'trucks': truck_list, 'trailers': trailer_list})
