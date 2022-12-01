class Login:
    def __init__(self, username:str, password:str):
        self.username = username
        self.password = password
        self.isLoggedIn = self.__login_admin()

    def __load_admin_database(self):
        """
        Retrieves credentials from database and stores them in a dictionary.\n
        Input: none\n
        Output: Returns a list of credential dictionaries,
        False if unable to retrieve data from database (text file).
        """
        admins = []
        try:
            with open("./passcodes.txt") as admin_file:
                for admin_data in admin_file:
                    uname_upass = admin_data.split(",")
                    admin_dict = {
                        "username": uname_upass[0].strip(),
                        "password": uname_upass[1].strip()
                    }
                    admins.append(admin_dict)
        except:
            raise Exception("💥 ERROR: Database unavailable. Please try again later or contact an administrator if the problem persists. 💥")
        else:
            return admins

    def __login_admin(self) -> bool:
        """
        Validates login info against admin database.\n
        Input: Admin database as list of credential dictionaries.\n
        Output: Returns True if login valid, False otherwise.
        """
        try:
            admin_database = self.__load_admin_database()
        except Exception as ex:
            raise Exception(ex)
        else:
            for admin in admin_database:
                if admin["username"] == self.username and admin["password"] == self.password:
                    return True
            return False