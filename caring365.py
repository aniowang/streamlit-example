import pandas as pd,os,streamlit as st
# import sqlite3 
# import SenaoDB
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)


#連接DB
def sqliteConnection():
    global connsqlite
    try:
        connsqlite.close()
    except:
        pass
    connsqlite=None
    try:
        if connsqlite is None:
            connsqlite=sqlite3.connect(r'C:\Users\018363\Project\20230617_sqlite3\Lab.db') 
    except:
        pass

def main(): 
       
    #添加側邊攔
    st.sidebar.title('選單')
    st.sidebar.write('測試版本：V0.0.2') 
    st.sidebar.write('測試時間：2024/5/3') 
    #操作說明
    with st.expander("操作說明"):
        st.write('1.登入後須點擊連線Sqlite資料庫方可查詢模型資訊')
        st.write('2.Sqlite連線狀態表示目前連線狀態')
        st.write('3.模型指標分類選擇"模型輸出"，可以檢視模型解釋資訊')
        st.write('4.點擊"展開資料集描述分頁"，可以檢視EDA結果')
    # #讀取EDW資料
    # edw_connect=st.button('連線EDW')
    # edw_connect_close=None
    # edw_connect_result=None    
    # if edw_connect:
    #     edw_connect_close=st.button('關閉連線EDW')
    #     try:
    #         db=SenaoDB.DB()
    #         conn=db._conn
    #         cur=db.cursor
    #         edw_connect_result='連線成功'
    #     except:
    #         edw_connect_result='連接失敗'
    # if edw_connect_close:
    #     try:
    #         db.close()
    #         edw_connect_result=None
    #     except:
    #         pass        
    # st.write('EDW連線狀態：',edw_connect_result)  
    # TAtable=None
    # query_result=None
    # TAtable=st.text_input('想查詢的模型：')
    # # TAtable='anio_model61v11_0429'
    # if TAtable:
    #     try:
    #         sql=f"""
    #         select sum(1) as 人數 from ptest.{TAtable} ;
    #         """
    #         query_result=pd.read_sql(sql,conn)
    #         st.write('查詢結果：',query_result)
    #     except:
    #         print('連線失敗或查詢失敗')
    #         query_result=None
    #         st.write('查詢結果：',query_result)   
    
    #讀取Sqlite資料庫
    sqlite_connect=st.sidebar.toggle('連線Sqlite資料庫')
    sqlite_connect_close=None
    sqlite_connect_result=None            
    if sqlite_connect:
        # sqlite_connect_close=st.button('關閉連線Sqlite資料庫')
        try:
            sqliteConnection()
            sqlite_connect_result='連線成功'
        except:
            sqlite_connect_result='連接失敗'
    if sqlite_connect_close:
        try:
            connsqlite.close()
            sqlite_connect_result=None
        except:
            pass  
    #連線狀態
    st.sidebar.write('Sqlite連線狀態：',sqlite_connect_result)
    if sqlite_connect_result:
        st.success('連線成功')
    else :
        st.warning('尚未連線，請由左側選單點擊連線Sqlite資料庫')
    
    sqlite_TAtable=None
    sqlite_query_result=None    
    sqlite_TAtable_Year=None
    sqlite_TAtable_Month=None
    sqlite_TAtable_category=None
    
    #版面分割：3行
    col1, col2, col3 = st.columns(3)
    
    with col1:
        years=['202308','202309','202310','202311','202312','202401','202402','202403','202404','202405']
        sqlite_TAtable_YM=st.selectbox('模型批次_年月',years)
        batch_num=None
        
    with col2:
        sqlite_TAtable_category=st.selectbox('模型指標分類',['模型特徵','模型評估','模型訓練','模型參數','模型輸出'])
    
    with col3:
        sqlite_TAtable_model=None
        models=['果粉','星粉','保健粉','遊戲粉','高資費','中低資費','蘋果電池螢幕','三星健檢','生活日用品']
        sqlite_TAtable_model=st.selectbox('模型名稱',models)
        
    try:
        num_model=53+models.index(sqlite_TAtable_model)
        batch_num=2+years.index(sqlite_TAtable_YM)
    except:
        st.write('指定模型：',sqlite_TAtable_model) 
    
    sqlite_TAtable=sqlite_TAtable_YM+sqlite_TAtable_category
    # st.write('查詢表單：',sqlite_TAtable) 

    if sqlite_TAtable:
        try:
            sql=f"""
            select * from "{sqlite_TAtable}" where "模型名稱" like '%{num_model}%';
            """
            sqlite_query_result=pd.read_sql(sql,connsqlite)
            st.write('查詢結果：',sqlite_query_result)
        except:
            st.write('連線失敗或查詢失敗')
            # query_result=None
            st.write('查詢結果：',sqlite_query_result) 
    
    if sqlite_TAtable_category =='模型輸出':
        pic_cat=st.selectbox('模型解釋',['Shape Value Summary','Decision tree'])
        if pic_cat == 'Shape Value Summary':
            pictype = 'summaryplot.jpg'
        elif pic_cat == 'Decision tree':
            pictype = 'decisiontree.svg'
        else:
            pictype=None
        url=f"https://aniowang.github.io/senao.github.io/model{num_model}V{batch_num}_{pictype}"
        # st.write(url)
        # components.iframe('https://aniowang.github.io/senao.github.io/model53V1_summaryplot.jpg',
        #                  height=500)
        st.image(url)
        
    data_analysis_page=st.toggle('展開資料集描述分頁')
    
    if data_analysis_page:
        #版面分頁：2頁
        tab1, tab2  = st.tabs(['訓練資料','預測資料'])
        
        with tab1:
            web_url_train=f"https://aniowang.github.io/senao.github.io/model{num_model}V{batch_num}_Train.html"
            # st.write('訓練資料集描述：',web_url_train)
            components.iframe(web_url_train,height=600,scrolling=True)
        
        with tab2:      
            web_url_predict=f"https://aniowang.github.io/senao.github.io/model{num_model}V{batch_num}_Predict.html"
            # st.write('預測資料集描述：',web_url_predict)
            components.iframe(web_url_predict,height=600,scrolling=True)
            
            
if __name__=="__main__":
    st.title('Caring 365 儀錶板')
    #修改登入介面文字
    authenticator.login( 
        location='main',
        fields={'Form name':'登入', 'Username':'使用者名稱', 'Password':'密碼', 'Login':'確認登入'})    
    if st.session_state["authentication_status"]:
        authenticator.logout(location='sidebar',button_name='確認登出')
        st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
        #登入成功後才執行main()
        main() 
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
    
