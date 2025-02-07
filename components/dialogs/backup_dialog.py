from configs.icons import AppIcons
from configs.messages import AppMessages
from configs.structure import DataStructure
from configs import datasource, utils
import pandas as pd
import streamlit as st


def show(sheet,selected_span):
    """ Export Dialog."""
    app_lang = AppMessages(st.session_state.language)
    
    import_tab,export_tab=st.tabs([f"{app_lang.IMPORT_BUTTON} {AppIcons.IMPORT_PAGE}", f"{app_lang.EXPORT_BUTTON} {AppIcons.EXPORT_PAGE}"])
    
    with import_tab:
        dataframe = None
        uploaded_file = st.file_uploader(
            app_lang.IMPORT_TOOLTIP, accept_multiple_files=False
        )
        if uploaded_file is not None:
            file_type = uploaded_file.name.split(".")[-1]
            status_placeholder = st.empty()
            left,right = st.columns([7,3],vertical_alignment="bottom")
            with left,st.spinner(app_lang.LOADING_TOOLTIP, show_time=True):
                if file_type == "csv":
                    try:
                        dataframe = pd.read_csv(uploaded_file)
                    except Exception as e:
                        status_placeholder.error(e.args)
                elif file_type == "xlsx":
                    dataframe = pd.read_excel(uploaded_file)
                else: 
                    status_placeholder.warning(app_lang.UNSUPPORTED_TYPE)
            if dataframe is not None:
                load_btn = right.button(app_lang.IMPORT_BUTTON,use_container_width=True,type="primary",icon=AppIcons.IMPORT_PAGE)
                if load_btn:
                    with left,st.spinner(app_lang.LOADING_TOOLTIP, show_time=True):
                        pass
                        try:
                            for index, row in dataframe.iterrows():
                                sheet.loc[len(sheet)] = row
                        except Exception as e:
                            status_placeholder.warning(e.args)
                        
                        sheet.drop_duplicates(subset=["Id"],keep="first",inplace=True,ignore_index=True)
                        sheet['Date'] = pd.to_datetime(sheet['Date'], format="%d/%m/%Y")
                        sheet = sheet.sort_values(by=['Date'])
                        datasource.update_from(sheet)
                        st.cache_data.clear()
                        st.cache_resource.clear()
                        st.rerun(scope="app")


    with export_tab, st.spinner(app_lang.LOADING_TOOLTIP,show_time=True):
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

            data_export, file_name = utils.get_export_data(dataframe_show,file_type,app_lang)
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