
class Seat:

    def __init__(self, seat_id, floor_id, location):
        self.seat_id = seat_id
        self.floor_id = floor_id
        self.occupied = 0
        self.user_id = None
        self.outlet = 0
        self.location = location
        # self.row_loc = 0 
        # self.col_loc = 0 
