from datetime import datetime, time
import streamlit as st

class DataStructure:
    """
    Initials Structures for objects.

    """
    @staticmethod
    def get_error_object(gsheet_state,gsheet_err):
        """ Compact gspread error into an object.

        Args:
            gsheet_state (boolean): Connection state.
            gsheet_err (object): Exceptions.

        Returns:
            dict: Error object.
        """
        return {
                "GSheet": {
                  "connected":gsheet_state,
                  "error": gsheet_err
                }
                }
    @staticmethod
    def get_export_type():
        """ Return export types.

        Returns:
            dict: Indext and file types.
        """
        return {
                0: ".csv",
                1: ".xlsx",
                2: ".xml",
                3: ".parquet",
                4: ".orc"
                }
    @staticmethod
    def get_categories():
        """ Return list of columns.

        Returns:
            list: Column list.
        """
        return ['Date', 'Spent', 'Type', 'Note']
    @staticmethod
    def get_column_configs():
        """ Return config of Columns in Streamlit dataframe API.

        Returns:
            dict: Column configs.
        """
        return {'Date': st.column_config.DatetimeColumn(
                    format='DD/MM/YYYY',
                    max_value=datetime.combine(datetime.now(), time.max),
                ),
                'Spent': st.column_config.NumberColumn(min_value=0, default=0,required=False),
                'Type': st.column_config.TextColumn(),
                'Note':  st.column_config.TextColumn()
                }
    
    @staticmethod
    def get_option_map()-> list:
        """ Return option mapping for expense types.

        Returns:
            dict: Options.
        """
        return {
            0: "Food",
            1: "Rent",
            2: "Traverse",
            3: "Subscriptions",
            4: ":material/add:"
        }

    @staticmethod
    def get_initial_data():
        """ Initiatal data for inserting.

        Returns:
            dict: 1 data row.
        """
        return {
            "Date": datetime.today().strftime("%d/%m/%Y"),
            "Spent": 0,
            "Type": "",
            "Note": ""
        }
    @staticmethod
    def get_initial_statistics(sheet="",total=0,highest=0,highest_category="",highest_category_value=0):
        """ Initiatal data for calculate statistics.

        Args:
            sheet (str, optional): Spreadsheet name. Defaults to "".
            total (int, optional): Total spent. Defaults to 0.
            highest (int, optional): Highest spent. Defaults to 0.
            highest_category (str, optional): Highest Spent of a certain category name. Defaults to "".
            highest_category_value (int, optional): Highest Spent of a certain category value. Defaults to 0.

        Returns:
            dict: Statistics Object.
        """
        return {
            "Sheet": sheet,
            "Total": total,
            "Highest": highest,
            "Highest_Category": highest_category,
            "Highest_Category_Value": highest_category_value
        }
    @staticmethod
    def get_convert_dict():
        """ Define value types.

        Returns:
            dict: Types.
        """
        return {
            'Spent': int,
            'Type': str,
            'Note': str,
        }