from app.api import bp


# All available transport(trucks, trailers, etc.)
@bp.route('/transport', methods=['GET'])
def get_transport():
    pass


# All available transport with selected type
@bp.route('/transport/<str:transport_type>', methods=["GET"])
def get_transport_selected_type(transport_type):
    pass


# Information about specific vehicle
@bp.route('/transport/<str:transport_type>/<specific_vehicle>', methods=["GET"])
def get_transport_selected_type(transport_type, current_vehicle):
    pass
