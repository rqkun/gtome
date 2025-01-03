from datetime import datetime, time
import streamlit as st

class DataStructure:
    @staticmethod
    def get_categories():
        return ['Date', 'Food', 'Rent', 'Traverse', 'Subscriptions', 'Misc', 'Fun', 'Note']
    
    @staticmethod
    def get_column_configs():
        numeric_config = st.column_config.NumberColumn(min_value=0, default=0,required=False)
        return {'Date': st.column_config.DatetimeColumn(
                    format='DD/MM/YYYY',
                    max_value=datetime.combine(datetime.now(), time.max),
                ),
                'Food': numeric_config,
                'Rent': numeric_config,
                'Traverse': numeric_config,
                'Subscriptions': numeric_config,
                'Misc': numeric_config,
                'Note':  st.column_config.TextColumn()
                }
    
    @staticmethod
    def get_statistic_categories():
        return ['Sheet', 'Total', 'Highest', 'Highest_Category', 'Highest_Category_Value']
    @staticmethod
    def get_statistic_dict():
        return {
            'Sheet': str,
            'Total': int,
            'Highest': int,
            'Highest_Category': str,
            'Highest_Category_Value': int
        }
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
    def get_initial_statistics(sheet="",total=0,highest=0,highest_category="",highest_category_value=0):
        return {
            "Sheet": sheet,
            "Total": total,
            "Highest": highest,
            "Highest_Category": highest_category,
            "Highest_Category_Value": highest_category_value
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