from configs.icons import AppIcons
from configs.messages import AppMessages
from configs.structure import DataStructure
from configs import utils
import pandas as pd
import streamlit as st


def show(sheet,selected_span):
    """ Export Dialog."""
    app_lang = AppMessages(st.session_state.language)
    export_placeholder = st.empty()
    if len(sheet) > 0:
        left,right = st.columns([5,2],vertical_alignment="bottom")
        if st.toggle(app_lang.EXPORT_TOGGLE_TOOLTIP):
            dataframe_show = sheet
        else:
            dataframe_show,_ = utils.filter(sheet,selected_span)
        dataframe_show = pd.DataFrame(dataframe_show).sort_values("Date",ascending=False)

        file_type = left.segmented_control(app_lang.EXPORT_TYPE_TOOLTIP_NAME,
                               options=DataStructure.get_export_type().keys(),
                               format_func=lambda option: DataStructure.get_export_type()[option],
                               selection_mode="single",
                               default=0,
                               help=app_lang.EXPORT_TYPE_TOOLTIP)

        data_export, file_name = utils.get_export_data(dataframe_show,file_type)
        right.download_button(label=app_lang.EXPORT_BUTTON,
                           data=data_export,
                           file_name=file_name,
                           use_container_width=True,
                           type="primary",
                           icon=AppIcons.EXPORT_PAGE)
        st.expander(app_lang.EXPANDER).dataframe(dataframe_show,
                    use_container_width=True,
                    hide_index=True
                    )
    else:
        export_placeholder.warning(app_lang.WARNING_SHEET_EMPTY,icon=AppIcons.ERROR)