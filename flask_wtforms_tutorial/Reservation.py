class Reservation:
    def __init__(self):
        self.cost_matrix = self.__get_cost_matrix()
        self.reservations = self.__load_reservations()
        self.bus_map = self.__get_bus_map()
        
    def __get_cost_matrix(self):
        """
        Generates cost matrix for bus.\n
        Input: none\n
        Output: Returns a 12 x 4 matrix of prices.
        """
        cost_matrix = [[100, 75, 50, 100] for row in range(12)]
        return cost_matrix

    def __load_reservations(self):
        """
        Retrieves reservations from database.\n
        Input: None\n
        Output: Returns reservations as list of reservation dictionaries,
        with keys (first_name, row, seat, e-ticket); otherwise,
        raises an exception if unable to retrieve data from database (text file).
        """
        reservations = []
        try:
            with open("./reservations.txt") as reservation_file:
                for reservation in reservation_file:
                    reservation_data = reservation.split(",")
                    reservation_dict = {
                        "first_name": reservation_data[0].strip(),
                        "row": int(reservation_data[1]),
                        "seat": int(reservation_data[2]),
                        "e-ticket": reservation_data[3].strip()
                    }
                    reservations.append(reservation_dict)
        except:
            raise Exception("💥 ERROR: Reservation database unavailable.  Please try again later or contact an administrator if the problem persists. 💥")
        else:
            return reservations

    def __get_bus_map(self):
        """
        Generates seat list and adds 'X' where seats are reserved.\n
        Input: None
        Output: Returns seat list as list of string lists.
        """
        seat_list = [['O' for col in range(4)] for row in range(12)]

        for i in range(len(self.reservations)):
            seat_row = self.reservations[i]['row']
            seat = self.reservations[i]['seat']
            for _ in range(len(seat_list[0])):
                seat_list[seat_row][seat] = 'X'

        return seat_list

    def __generate_eticket(self) -> str:
        """
        Merges user first name and course to simulate e-ticket.\n
        Input: None
        Output: Returns e-ticket as string.
        """
        name_array = [char for char in self.first_name]
        course_array = [char for char in "INFOTC4320"]

        merged = []
        if len(course_array) > len(name_array):
            for i in range(len(course_array)):
                if i < len(name_array):
                    merged.append(name_array[i])
                    merged.append(course_array[i])
                else:
                    merged.append(course_array[i])
        else:
            for i in range(len(name_array)):
                if i < len(course_array):
                    merged.append(name_array[i])
                    merged.append(course_array[i])
                else:
                    merged.append(name_array[i])
        return "".join(merged)

    def __check_seat_availability(self, row:int, seat:int) -> bool:
        """
        Checks user seat request against saved reservations.\n
        Input: User's row and seat request as integers.\n
        Output: Returns True if requested seat is available, False if already reserved.
        """
        for i in range(len(self.reservations)):
            if row == self.reservations[i]['row']:
                if seat == self.reservations[i]['seat']:
                    return False
        return True

    def __persist_reservation(self) -> bool:
        """
        Saves reservation to database (text file).\n
        Input: None\n
        Output: Returns True if successful, False if unsuccessful.
        """
        try:
            with open("./reservations.txt", "a") as reservation_file:
                reservation = f"{self.first_name}, {self.row}, {self.seat}, {self.e_ticket}\n"
                reservation_file.write(reservation)
                return True
        except:
            return False
    
    def make_reservation(self, first_name:str, last_name:str, row:int, seat:int) -> str:
        """
        Reserves a seat on the bus for the user.\n
        Input: User's first and last name, requested row and seat number.\n
        Output: Returns a success string message if successful, raises an exception if unsuccessful.
        """
        total_seats = 48
        seats_remaining = total_seats - len(self.reservations)

        # Check if bus is sold out
        if seats_remaining != 0:
            self.first_name = first_name.title()
            self.last_name = last_name.title()
            self.row = row - 1
            self.seat = seat - 1
            # Check availability
            if self.__check_seat_availability(self.row, self.seat):
                # Generate e-ticket
                self.e_ticket = self.__generate_eticket()
                # Persist reservation to database (text file in this case)
                if self.__persist_reservation():
                    # Update current reservations and bus map with new reservation info
                    self.reservations.append({
                        "first_name": self.first_name,
                        "row": self.row,
                        "seat": self.seat,
                        "e-ticket": self.e_ticket
                    })
                    self.bus_map = self.__get_bus_map()
                    return f"Congratulations {self.first_name.title()}! Row:  {row} Seat:  {seat} is now reserved for you!  Enjoy the trip!"
                else:
                    raise Exception("💥 ERROR: Reservation database unavailable.  Please try again later or contact an administrator if the problem persists. 💥")
            else:
                raise Exception(f"\nRow:  {row} Seat:  {seat}, is already assigned. Choose again.\n")
        else:
            raise Exception("Sorry, this bus is full.")

    def calculate_total_sales(self) -> float:
        """
        Iterates through bus map looking for 'X's. When found,
        gets cost from cost matrix at that seat location and adds to total.\n
        Input: Bus map as list of string lists.\n
        Output: Returns total cost of all reserved seats as float.
        """
        total = 0.0

        for row in range(len(self.bus_map)):
            for seat in range(len(self.bus_map[0])):
                if self.bus_map[row][seat] == 'X':
                    total += self.cost_matrix[row][seat]

        return total