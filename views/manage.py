import streamlit as st
from datetime import datetime, time
from classes.icons import AppIcons
from classes.messages import AppMessages
import lib.datasource as datasource
import lib.headers as header

def find_key(list_str,value):
    try:
        return list_str.index(value)
    except:
        return len(list_str)-1

def not_saved():
    st.warning('Changes you made have not been saved!', icon=AppIcons.WARNING)

def numeric_config():
    return st.column_config.NumberColumn(min_value=0, default=0,required=False)


header.add_header()

if 'sheet_key' not in st.session_state:
    st.session_state['sheet_key'] =datetime.today().strftime('%B-%Y')
try:
    conn,worksheet_names = datasource.get_sheets()
    if 'sheet' not in st.session_state:
        st.session_state['sheet'] = datasource.clean(conn.read(worksheet=st.session_state['sheet_key']))
except ConnectionError as err:
    st.error(AppMessages.get_connecition_errors(err.args),icon=AppIcons.ERROR)

sheet = st.session_state['sheet']

col1,col2,col3 = st.columns([3,1,1])
placeholder = st.empty()
option = col1.selectbox(label="Sheet Select",
                        options = worksheet_names,
                        index=find_key(worksheet_names,st.session_state['sheet_key']),
                        label_visibility="collapsed"
                        )

if col2.button("Sync",use_container_width=True, icon=AppIcons.SYNC,type="primary"): 
    placeholder.empty()
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()
    
update_button = col3.button("Save",use_container_width=True,type="primary",icon=AppIcons.SAVE)
convert_dict = {'Date': st.column_config.DatetimeColumn(
                            format='DD/MM/YYYY',
                            min_value=datetime.strptime("1-"+option,'%d-%B-%Y'),
                            max_value=datetime.combine(datetime.now(), time.max),
                        ),
                        'Food': numeric_config(),
                        'Rent': numeric_config(),
                        'Traverse': numeric_config(),
                        'Subscriptions': numeric_config(),
                        'Misc': numeric_config(),
                        'Note':  st.column_config.TextColumn()
                        }
if option:
    sheet = datasource.read_from(conn,option)
    st.session_state['sheet'] = sheet

tmp_df = placeholder.data_editor(st.session_state['sheet'],
                        use_container_width=True,
                        height=35*len(st.session_state['sheet'])+36*2,
                        hide_index=True,
                        column_config=convert_dict,
                        on_change=not_saved,
                        num_rows='dynamic')

st.session_state['sheet'] = datasource.clean(tmp_df)

if update_button: 
    datasource.update_from(conn,option,None)
    print(st.session_state['sheet'])
    st.cache_data.clear()
    st.rerun()