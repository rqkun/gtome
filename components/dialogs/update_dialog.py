from datetime import datetime
from configs import datasource
from configs.icons import AppIcons
from configs.messages import AppMessages
from configs.structure import DataStructure
from configs import utils
import pandas as pd
import streamlit as st


def show(sheet,selected_span):
    """ Update Dialog."""
    app_lang = AppMessages(st.session_state.language)
    try:
        saved = False
        sheet["Type"] = sheet["Type"].astype(str)
        data_update, remaining = utils.filter(sheet,selected_span)
        update_placeholder = st.empty()
        update_form = st.form("update_form",clear_on_submit=True,enter_to_submit=True)
        tmp_df = update_form.data_editor(data_update,
                                use_container_width=True,
                                height=35*len(data_update)+36*2,
                                hide_index=True,
                                column_order=("Date","Spent","Type","Note"),
                                column_config=DataStructure.get_column_configs(),
                                num_rows='dynamic')

        if update_form.form_submit_button(app_lang.SAVE_BUTTON, use_container_width=True, type="primary", icon=AppIcons.SAVE):
            # Add updated data_update back to sheet
            with st.spinner(app_lang.LOADING_TOOLTIP, show_time=True):
                update = pd.concat([remaining, tmp_df], ignore_index=True)
                datasource.update_from(update)
                saved = True
                st.cache_data.clear()
                st.cache_resource.clear()
                st.rerun(scope="app")
        if saved ==False:
            raise ValueError(app_lang.WARNING_CHANGES_NOT_SAVED)
    except ValueError as err:
        update_placeholder.warning(err.args[0],icon=AppIcons.ERROR)

def single(df,row_data):
    app_lang = AppMessages(st.session_state.language)
    try:
        row = row_data.copy()
        trash,header = st.columns([1,9],vertical_alignment="bottom")
        header.subheader(row["Id"],None,divider="red")
        delete_bttn = trash.button(AppIcons.TRASH,use_container_width=True,type='secondary')
        amount = st.number_input(app_lang.AMOUNT_TOOLTIP_NAME,min_value=0,
                                 step=1000,help=app_lang.AMOUNT_TOOLTIP,
                                 value=int(row["Spent"]))
        
        type_of_expense = st.text_input(app_lang.TYPE_TOOLTIP_NAME,max_chars=20,placeholder="Misc",value=row["Type"])
        
        st.write(app_lang.DATEINPUT_TOOLTIP_NAME)
        date = st.date_input("Document Date",
                                      format="DD/MM/YYYY",
                                      label_visibility="collapsed",value=row["Date"])

        st.write(app_lang.NOTE_TOOLTIP_NAME)
        left_insert,right_insert = st.columns([5,2])
        notes = left_insert.text_input(app_lang.NOTE_TOOLTIP_NAME,placeholder=app_lang.NOTE_TOOLTIP,label_visibility='collapsed',value=row["Note"])
        submit_bttn = right_insert.button(app_lang.SAVE_BUTTON,
                                          use_container_width=True,
                                          icon=AppIcons.SAVE,
                                          type="primary")

        if type_of_expense is None or type_of_expense =="":
            raise ValueError(app_lang.INVALID_EXPENSE_TYPE)
            
        if submit_bttn:
            with st.spinner(app_lang.LOADING_TOOLTIP, show_time=True):
                df.loc[df["Id"] == row["Id"], ["Date", "Spent", "Type", "Note"]] = (
                    date.strftime("%Y-%m-%d"), amount, type_of_expense, notes
                )
                df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
                df = df.sort_values(by=['Date'])
                datasource.update_from(df)
                st.cache_data.clear()
                st.cache_resource.clear()
            st.rerun(scope="app")
            
        if delete_bttn:
            with st.spinner(app_lang.LOADING_TOOLTIP, show_time=True):
                df = df.drop(df[df["Id"] == row["Id"]].index)
                df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
                df = df.sort_values(by=['Date'])
                datasource.update_from(df)
                st.cache_data.clear()
                st.cache_resource.clear()
            st.rerun(scope="app")
            
    except ValueError as err:
        st.error(app_lang.get_validation_errors(err.args),icon=AppIcons.ERROR)