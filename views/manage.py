""" Management page for the data grid. """

import calendar
from datetime import datetime
import streamlit as st
from classes.icons import AppIcons
from classes.messages import AppMessages
from classes.structure import DataStructure
import lib.datasource as datasource
import lib.headers as header

def not_saved():
    """ Show warning when not saved. """
    st.warning(AppMessages.WARNING_CHANGES_NOT_SAVED, icon=AppIcons.WARNING)

header.add_header()

try:
    sheet = datasource.get_detail_sheets()
except ConnectionError as err:
    st.error(AppMessages.get_connection_errors(err.args),icon=AppIcons.ERROR)

col1,col2,col3 = st.columns([3,1,1],vertical_alignment="bottom")
placeholder = st.empty()

today = datetime.now()
start_date = today.replace(day=1)
last_day = calendar.monthrange(today.year, today.month)[1]
end_date = today.replace(day=last_day)

selected_span = col1.date_input(
    "Select your expense span",
    (start_date, end_date),
    format="DD/MM/YYYY",
)


if col2.button("Sync",use_container_width=True, icon=AppIcons.SYNC,type="primary"):
    placeholder.empty()
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

update_button = col3.button("Save",use_container_width=True,type="primary",icon=AppIcons.SAVE)


if len(selected_span) < 2:
    st.warning(AppMessages.INVALID_DATE, icon=AppIcons.WARNING)
else: 
    data = datasource.filter(sheet,selected_span)
    
    tmp_df = placeholder.data_editor(data,
                            use_container_width=True,
                            height=35*len(data)+36*2,
                            hide_index=True,
                            column_config=DataStructure.get_column_configs(),
                            on_change=not_saved,
                            num_rows='dynamic')
    
    if update_button:
        datasource.update_from(tmp_df,data,sheet)
        placeholder.empty()
        st.cache_data.clear()
        st.rerun()
