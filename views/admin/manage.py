import streamlit as st
from datetime import datetime
import lib.common as common


def find_key(list_str,value):
    try:
        return list_str.index(value)
    except:
        return len(list_str)-1

def not_saved():
    st.warning('Changes you made have not been saved!', icon="⚠️")

conn,worksheet_names = common.get_sheets()

if 'sheet_key' not in st.session_state:
    st.session_state['sheet_key'] =datetime.today().strftime('%B-%Y')

if 'sheet' not in st.session_state:
    st.session_state['sheet'] = common.clean(conn.read(worksheet=st.session_state['sheet_key']))
    



col1,col2 = st.columns([6,1])

sheet = st.session_state['sheet']


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
    update_button = st.button("Save",use_container_width=True,type="primary",icon=":material/sync:")
    
convert_dict = {    'Date': st.column_config.DatetimeColumn(
                            format='DD/MM/YYYY',
                            min_value=datetime.strptime("1-"+option,'%d-%B-%Y'),
                            max_value=datetime.strptime("30-"+option,'%d-%B-%Y')
                        ),
                        'Food': st.column_config.NumberColumn(
                            min_value=0,
                        ),
                        'Rent':  st.column_config.NumberColumn(
                            min_value=0,
                        ),
                        'Traverse':  st.column_config.NumberColumn(
                            min_value=0,
                        ),
                        'Subscriptions':  st.column_config.NumberColumn(
                            min_value=0,
                        ),
                        'Misc':  st.column_config.NumberColumn(
                            min_value=0,
                        ),
                        'Note':  st.column_config.TextColumn()
                        }

tmp_df = st.data_editor(st.session_state['sheet'],
                        use_container_width=True,
                        height=35*len(st.session_state['sheet'])+38,
                        hide_index=True,
                        column_config=convert_dict,
                        on_change=not_saved,
                        num_rows='dynamic')

st.session_state['sheet'] = tmp_df

if update_button: 
    conn.update(
        worksheet=option,
        data=st.session_state['sheet']
        
    )
    print(st.session_state['sheet'])
    st.cache_data.clear()
    st.rerun()