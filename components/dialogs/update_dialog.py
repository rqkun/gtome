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
                                column_config=DataStructure.get_column_configs(),
                                num_rows='dynamic')

        if update_form.form_submit_button(app_lang.SAVE_BUTTON, use_container_width=True, type="primary", icon=AppIcons.SAVE):
            # Add updated data_update back to sheet
            with st.spinner(app_lang.LOADING_TOOLTIP, show_time=True):
                update = pd.concat([remaining, tmp_df], ignore_index=True)
                datasource.update_from(update)
                saved = True
                st.cache_data.clear()
                st.rerun(scope="app")
        if saved ==False:
            raise ValueError(app_lang.WARNING_CHANGES_NOT_SAVED)
    except ValueError as err:
        update_placeholder.warning(err.args[0],icon=AppIcons.ERROR)