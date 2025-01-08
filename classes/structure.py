from datetime import datetime, time
import streamlit as st

class DataStructure:
    @staticmethod
    def get_export_type():
        return {
                0: ".csv",
                1: ".xlsx",
                2: ".xml",
                3: ".parquet",
                4: ".orc"
                }
    @staticmethod
    def get_categories():
        return ['Date', 'Spent', 'Type', 'Note']
    @staticmethod
    def get_column_configs():
        return {'Date': st.column_config.DatetimeColumn(
                    format='DD/MM/YYYY',
                    max_value=datetime.combine(datetime.now(), time.max),
                ),
                'Spent': st.column_config.NumberColumn(min_value=0, default=0,required=False),
                'Type': st.column_config.TextColumn(),
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
    def get_option_map():
        return {
            0: "Food",
            1: "Rent",
            2: "Traverse",
            3: "Subscriptions",
            4: ":material/add:"
        }

    @staticmethod
    def get_initial_data():
        return {
            "Date": datetime.today().strftime("%d/%m/%Y"),
            "Spent": 0,
            "Type": "",
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
            'Spent': int,
            'Type': str,
            'Note': str,
        }