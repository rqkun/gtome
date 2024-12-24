import streamlit as st
from datetime import datetime
import lib.common as common
import lib.headers as header

@st.dialog("Insert Data")
def insert(conn,df,option):
    option_map, initial_data = common.set_up()
    amount = st.number_input("Amount",min_value=0,step=1000,help="Amount should be in VND",placeholder="50000")
    type_of_expense = st.pills("Type of Expense",
                                options=option_map.keys(),
                                format_func=lambda option: option_map[option],
                                selection_mode="single",
                                default=4
                            )
    notes = st.text_input("Notes",placeholder="Input note here...")
    
    st.write("Document Date:")
    col1,col2 = st.columns([5,2])
    with col1:
        date = st.date_input("Document Date", "today", format="DD/MM/YYYY",label_visibility="collapsed")
    with col2:
        submit_bttn = st.button('Submit',use_container_width=True,icon=":material/done_outline:",type="primary")
       
    if submit_bttn:
        
        initial_data[option_map[type_of_expense]] = amount
        initial_data["Date"] = date.strftime("%d/%m/%Y")
        initial_data["Note"] = notes
        df.loc[len(df)] = initial_data
        df = df.sort_values(by=['Date'])
        conn.update(
            worksheet=option,
            data=df,
        )
        st.cache_data.clear()
        st.rerun()


conn,worksheet_names = common.get_sheets()
header.add_header()

if 'sheet_key' not in st.session_state:
    st.session_state['sheet_key'] =datetime.today().strftime('%B-%Y')

if 'sheet' not in st.session_state:
    st.session_state['sheet'] = common.clean(conn.read(worksheet=st.session_state['sheet_key']))
    

col1,col2 = st.columns([6,1])

sheet = st.session_state['sheet']



with col1:
    option = st.selectbox(label="Sheet Select",
                        options = worksheet_names,
                        index=common.find_key(worksheet_names,st.session_state['sheet_key']),
                        label_visibility="collapsed"
                    )
    if option:
        sheet = common.clean(conn.read(worksheet=option))
        st.session_state['sheet'] = sheet
    

with col2:
    insert_button = st.button("Insert",use_container_width=True, icon=":material/add_task:",type="primary")
    if insert_button: 
        insert(conn,sheet,option)


st.dataframe(sheet,use_container_width=True,height=35*len(sheet)+38,hide_index=True) 






