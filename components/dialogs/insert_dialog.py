
import pandas as pd
import streamlit as st
from configs.icons import AppIcons
from configs.messages import AppMessages
from configs import datasource
import uuid

def show(df):
    """
        Create a insert dialog form
    """
    app_lang = AppMessages(st.session_state.language)
    try:
        option_map, initial_data = datasource.set_up_data()
        amount = st.number_input(app_lang.AMOUNT_TOOLTIP_NAME,min_value=0,
                                 step=1000,help=app_lang.AMOUNT_TOOLTIP,
                                 placeholder="50000")
        type_of_expense = st.pills(app_lang.TYPE_TOOLTIP_NAME,
                                    options=option_map.keys(),
                                    format_func=lambda option: option_map[option],
                                    selection_mode="single",
                                    default=0
                                )
        extra_type = st.empty()
        st.write(app_lang.DATEINPUT_TOOLTIP_NAME)
        date = st.date_input("Document Date",
                                      "today",
                                      format="DD/MM/YYYY",
                                      label_visibility="collapsed")

        st.write(app_lang.NOTE_TOOLTIP_NAME)
        left_insert,right_insert = st.columns([5,2])
        notes = left_insert.text_input(app_lang.NOTE_TOOLTIP_NAME,placeholder=app_lang.NOTE_TOOLTIP,label_visibility='collapsed')
        submit_bttn = right_insert.button(app_lang.SAVE_BUTTON,
                                          use_container_width=True,
                                          icon=AppIcons.SAVE,
                                          type="primary")

        if type_of_expense is None:
            raise ValueError(app_lang.INVALID_EXPENSE_TYPE)
        elif type_of_expense == 4:
            expense_type = extra_type.text_input(app_lang.OTHER_TYPE_TOOLTIP_NAME,"Misc",20,placeholder="Misc")
        else:
            expense_type =  option_map[type_of_expense]
            
        if submit_bttn:
            with st.spinner(app_lang.LOADING_TOOLTIP, show_time=True):
                initial_data = (
                    uuid.uuid4(),date.strftime("%d/%m/%Y"), amount, expense_type, notes
                )

                df.loc[len(df)] = initial_data
                df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
                df = df.sort_values(by=['Date'])
                datasource.update_from(df)
                st.cache_data.clear()
                st.cache_resource.clear()
            st.rerun()
    except ValueError as err:
        st.error(app_lang.get_validation_errors(err.args),icon=AppIcons.ERROR)

