import datetime

class DataStructure:
    @staticmethod
    def get_categories():
        return ['Date', 'Food', 'Rent', 'Traverse', 'Subscriptions', 'Misc', 'Fun', 'Note']
    @staticmethod
    def get_categories_numeric():
        return ['Food', 'Rent', 'Traverse', 'Subscriptions', 'Misc', 'Fun']

    @staticmethod
    def get_option_map():
        return {
            0: "Food",
            1: "Rent",
            2: "Traverse",
            3: "Subscriptions",
            4: "Misc",
            5: "Fun"
        }

    @staticmethod
    def get_initial_data():
        return {
            "Date": datetime.today().strftime("%d/%m/%Y"),
            "Food": 0,
            "Rent": 0,
            "Traverse": 0,
            "Subscriptions": 0,
            "Misc": 0,
            "Fun": 0,
            "Note": ""
        }

    @staticmethod
    def get_convert_dict():
        return {
            'Food': int,
            'Rent': int,
            'Traverse': int,
            'Subscriptions': int,
            'Misc': int,
            'Fun': int,
            'Note': str,
        }