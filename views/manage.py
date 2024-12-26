import streamlit as st
from datetime import datetime, time
from classes.messages import MessageConstants
import lib.common as common
import lib.headers as header

def find_key(list_str,value):
    try:
        return list_str.index(value)
    except:
        return len(list_str)-1

def not_saved():
    st.warning('Changes you made have not been saved!', icon="⚠️")

def numeric_config():
    return st.column_config.NumberColumn(min_value=0, default=0,required=False)


header.add_header()

if 'sheet_key' not in st.session_state:
    st.session_state['sheet_key'] =datetime.today().strftime('%B-%Y')
try:
    conn,worksheet_names = common.get_sheets()
    if 'sheet' not in st.session_state:
        st.session_state['sheet'] = common.clean(conn.read(worksheet=st.session_state['sheet_key']))
except ConnectionError as err:
    st.error(MessageConstants.get_connecition_errors(err.args),icon=":material/error:")

sheet = st.session_state['sheet']

col1,col2 = st.columns([6,1])
with col1:
    option = st.selectbox(label="Sheet Select",
                        options = worksheet_names,
                        index=find_key(worksheet_names,st.session_state['sheet_key']),
                        label_visibility="collapsed"
                    )
    if option:
        sheet = common.clean(conn.read(worksheet=option))
        st.session_state['sheet'] = sheet
    
with col2:
    update_button = st.button("Save",use_container_width=True,type="primary",icon=":material/save_as:")
    
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

tmp_df = st.data_editor(st.session_state['sheet'],
                        use_container_width=True,
                        height=35*len(st.session_state['sheet'])+36*2,
                        hide_index=True,
                        column_config=convert_dict,
                        on_change=not_saved,
                        num_rows='dynamic')

st.session_state['sheet'] = common.clean(tmp_df)

if update_button: 
    conn.update(
        worksheet=option,
        data=st.session_state['sheet']
    )
    print(st.session_state['sheet'])
    st.cache_data.clear()
    st.rerun()