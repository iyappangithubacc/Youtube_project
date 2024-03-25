# Youtube Project-1

from googleapiclient.discovery import build
from pprint import pprint
import pymongo
from pymongo import MongoClient
import psycopg2
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import time

# API key: "AIzaSyB0wE2zRWb0VDimXJOn1PBOIikzrArWvp0"

#API key connection
def Api_connect():
    Api_id="AIzaSyB0wE2zRWb0VDimXJOn1PBOIikzrArWvp0"
    Api_service_name = "youtube"
    Api_version = "v3"
    
    youtube = build(Api_service_name,Api_version,developerKey=Api_id)
    return youtube
youtube=Api_connect()

# Get channel details
def Get_channel_details(Channel_id):
    request=youtube.channels().list(
                    part="snippet,contentDetails,statistics",
                    id=Channel_id  
    )
    response=request.execute()
    #pprint(response)
    
    for i in response['items']:
        Ch_data=dict(Ch_id=i['id'],
                    Ch_name=i["snippet"]["title"],
                    Subscribers=i['statistics']['subscriberCount'],
                    Views=i['statistics']['viewCount'],
                    Total_videos=i['statistics']['videoCount'],
                    Ch_descrip=i['snippet']['description'],
                    Upload_id=i['contentDetails']['relatedPlaylists']['uploads']
                    )
    return Ch_data
#Channel_data=Get_channel_details(Ch_Id)


# get channel playlist details:
def Get_playlist_details(Channel_id):
    
    global Playlist_ids
    
    Playlist_ids=[]
    Playlist_details=[]

    next_page_token=None
    
    while True:
        request = youtube.playlists().list(
                                            part="snippet,contentDetails",
                                            channelId=Channel_id,
                                            maxResults=50,
                                            pageToken=next_page_token
                                            )
        response = request.execute()
        #pprint(response)
        
        for a in response['items']:
            
            Playlist_ids.append(a['id'])
            
            Pl_details=dict(Pl_id=a['id'],
                            Ch_id=a['snippet']['channelId'],
                            Pl_name=a['snippet']['title'],
                            Video_count=a['contentDetails']['itemCount']
                            )
            
            Playlist_details.append(Pl_details)
            
        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            break
        
    #pprint(response)

    return Playlist_details
#Ch_playlist_details= Get_playlist_details(Ch_Id)


# Get video ids:
def Get_videos_ids(Channel_Id):
    Video_ids=[]
    request=youtube.channels().list(
                                id=Channel_Id,
                                part="contentDetails"
                                )
    response=request.execute()
    Ch_upload_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    #pprint(response)

    Nextpage_token=None
    
    while True:
        request1 = youtube.playlistItems().list(
                                                part="snippet",
                                                playlistId=Ch_upload_id,
                                                maxResults=50,
                                                pageToken=Nextpage_token
                                                )
        response1=request1.execute()
        #pprint(response1)
        for i in range(len(response1['items'])):
            R=response1['items'][i]['snippet']['resourceId']['videoId']
            Video_ids.append(R)
        Nextpage_token=response1.get('nextPageToken')
        
        if Nextpage_token is None:
            break
    return Video_ids   
#Video_Ids=Get_videos_ids(Ch_Id)


# Get video details with playlist ids:
def Get_video_details(Playlist_ids):
    
    Pid_of_Vids=[]
    Vid_of_Pids=[]

    for PL_Id in Playlist_ids:

        nextPageToken=None
        while True:
            PLI_request = youtube.playlistItems().list(
                                                        part="snippet",
                                                        playlistId=PL_Id,
                                                        maxResults=50,
                                                        pageToken=nextPageToken
                                                        )
            PLI_response=PLI_request.execute()
            #pprint(PLI_response)

            for item in PLI_response['items']:
                Pid_of_Vid=item['snippet']['playlistId']
                Vid_of_Pid=item['snippet']['resourceId']['videoId']
                if Vid_of_Pid not in Vid_of_Pids:
                    Pid_of_Vids.append(Pid_of_Vid)
                    Vid_of_Pids.append(Vid_of_Pid)
            
            nextPageToken=PLI_response.get('nextPageToken')
            if nextPageToken is None:
                break
            
    #print(Pid_of_Vids)
    #print(Vid_of_Pids)
    
    Videos_details=[]
    for Video_Id,PL_ID in zip(Vid_of_Pids,Pid_of_Vids):
        VD_request=youtube.videos().list(
                                    part="snippet,contentDetails,statistics",
                                    id=Video_Id
                                    )
        VD_response=VD_request.execute()
        #pprint(VD_response)
        
        for info in VD_response['items']:
            Video_data=dict(Video_id=info['id'],
                            Playlist_id=PL_ID,
                            Video_name=info['snippet']['title'],
                            Video_descrip=info['snippet'].get('description'),
                            Published_date=info['snippet']['publishedAt'],
                            View_count=info['statistics'].get('viewCount'),
                            Like_count=info['statistics'].get('likeCount'),
                            Favorite_count=info['statistics']['favoriteCount'],
                            Comment_count=info['statistics'].get('commentCount'),
                            Video_duration=info['contentDetails']['duration'],
                            Thumbnail=info['snippet']['thumbnails']['default']['url'],
                            Caption_status=info['contentDetails']['caption']
                            )
            Videos_details.append(Video_data)
        
    return Videos_details 
#Videos_details=Get_video_details(Playlist_ids)

        
# Get video commend details:
def Get_vcomment_details(Video_Ids):

    Vcomment_details=[]
    try:
        for Video_Id in Video_Ids:
            request=youtube.commentThreads().list(
                                        part="snippet",
                                        videoId=Video_Id,
                                        maxResults=50
                                        )
            response=request.execute()
            #pprint(response)
            
            for info in response['items']:
                Comment_data=dict(Comment_id=info['snippet']['topLevelComment']['id'],
                                Video_id=info['snippet']['topLevelComment']['snippet']['videoId'],
                                Comment_text=info['snippet']['topLevelComment']['snippet']['textDisplay'],
                                Comment_author=info['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                Comment_published_date=info['snippet']['topLevelComment']['snippet']['publishedAt']
                                )
                Vcomment_details.append(Comment_data)
    except:
        pass
    
    return Vcomment_details
#Video_comment_details=Get_vcomment_details(Video_Ids)


# Connect to Mongodb
Client=pymongo.MongoClient("mongodb+srv://Iyappan:iyappanmdb@cluster0.578ym4w.mongodb.net/?retryWrites=true&w=majority")
db=Client["Youtube_project1"]


# Get channel all details:
def Get_channel_all_details(Ch_Id):
    Ch_details=Get_channel_details(Ch_Id)
    AllPl_details=Get_playlist_details(Ch_Id)
    AllVideo_ids=Get_videos_ids(Ch_Id)
    AllVideo_details=Get_video_details(Playlist_ids)
    Allcomment_details=Get_vcomment_details(AllVideo_ids)
    

    collection1=db["Youtube_channel_details"]
    collection1.insert_one({"Channel_details":Ch_details,
                            "Playlist_details":AllPl_details,
                            "Video_details":AllVideo_details,
                            "Commend_details":Allcomment_details
                            })
    
    return "Channel details are uploaded successfully in MongoDB"



# Important PostgreSQL Connection Information:
#Host="localhost"
#Port="5432"
#User="postgres"
#Password="Iyappan"
#Database="postgres"

# SQL server connection:
def Connect_SQL_server():
    
    Connect_SQL=psycopg2.connect(host="localhost",
                            port="5432",
                            user="postgres",
                            password="Iyappan",
                            database="Youtube_project"
                            )
    Cursor=Connect_SQL.cursor()
    
    print("SQL Connection is successful")
    
    return Connect_SQL, Cursor
#Connect_SQL, Cursor=Connect_SQL_server()


# Load data into SQL: # 1 Channel Table
def Create_sqltable_channels():

    # SQL server connection:
    Connect_SQL, Cursor=Connect_SQL_server()

    # Delete sql table if exists:
    Drop_query='''drop table if exists channels cascade'''
    Cursor.execute(Drop_query)
    Connect_SQL.commit()

    # SQL Table creation:  
    try:   
        Create_T_Query='''create table if not exists channels(Ch_id varchar(100) primary key,
                                                        Ch_name varchar(250),
                                                        Subscribers bigint,
                                                        Views bigint,
                                                        Total_videos int,
                                                        Ch_descrip text,
                                                        Upload_id varchar(100)
                                                        )'''
        Cursor.execute(Create_T_Query)
        Connect_SQL.commit()
        
    except:
        print("Channel table already created")


    # Get data from Mongodb and convert it into Data frame:
    Channel_list=[]
    db=Client["Youtube_project1"]
    collection1=db["Youtube_channel_details"]
    
    for ch_data in collection1.find({},{"_id":0,"Channel_details":1}):
        Channel_list.append(ch_data["Channel_details"])
    df=pd.DataFrame(Channel_list)
    pprint(df)

    # Insert values to Mysql table:
    for index,row in df.iterrows():
        Insert_query='''insert into channels(Ch_id,
                                        Ch_name,
                                        Subscribers,
                                        Views,
                                        Total_videos,
                                        Ch_descrip,
                                        Upload_id)
                                        
                                        values(%s,%s,%s,%s,%s,%s,%s)'''
                                        
        values=(row['Ch_id'],
                row['Ch_name'],
                row['Subscribers'],
                row['Views'],
                row['Total_videos'],
                row['Ch_descrip'],
                row['Upload_id']
                )                                                                                                              
        
        try:
            Cursor.execute(Insert_query,values)
            Connect_SQL.commit()
            
        except:
            print("Channel values are already inserted")
    
    return "Channel table is created in SQL"
#InsertSQL_channels=Create_sqltable_channels()


# Load data into Sql: # 2 Playlist Table
def Create_sqltable_playlists():
    
    # SQL server connection:
    Connect_SQL, Cursor=Connect_SQL_server()

    # Delete sql table if exists:
    Drop_query='''drop table if exists playlist cascade'''
    Cursor.execute(Drop_query)
    Connect_SQL.commit()

    # SQL Table creation:  
    try:   
        Create_T_Query='''create table if not exists playlist(Pl_id varchar(100) primary key,
                                                        Ch_id varchar(100) references channels(Ch_id),
                                                        Pl_name text,
                                                        Video_count int                                                   
                                                        )'''
                                                        
        Cursor.execute(Create_T_Query)
        Connect_SQL.commit()
        
    except:
        print("Playlist table already created")


    # Get data from Mongodb and convert it into Data frame:
    Playlists=[]
    db=Client["Youtube_project1"]
    collection1=db["Youtube_channel_details"]

    for pl_data in collection1.find({},{"_id":0,"Playlist_details":1}):
        for ind in range(len(pl_data["Playlist_details"])):
            Playlists.append(pl_data["Playlist_details"][ind])
    df1=pd.DataFrame(Playlists)
    pprint(df1)

    # Insert values to Mysql table:
    for index,row in df1.iterrows():
        Insert_query='''insert into playlist(Pl_id,
                                                Ch_id,
                                                Pl_name,
                                                Video_count
                                                )
                                                values(%s,%s,%s,%s)'''
                                        
        values=(row['Pl_id'],
                row['Ch_id'],
                row['Pl_name'],
                row['Video_count']
                )
        
        try:
            Cursor.execute(Insert_query,values)
            Connect_SQL.commit()
            
        except:
            print("Playlist details are already inserted")
            
    return "Playlist table is created in SQL"
#InsertSQL_playlist=Create_sqltable_playlists()


# Load data into Sql: # 3 Video Table
def Create_sqltable_videos():
    
    # SQL server connection:
    Connect_SQL, Cursor=Connect_SQL_server()

    # Delete sql table if exists:
    Drop_query='''drop table if exists videos cascade'''
    Cursor.execute(Drop_query)
    Connect_SQL.commit()

    # SQL Table creation:  
    try:   
        Create_T_Query='''create table if not exists videos(Video_id varchar(100) primary key,
                                                        Playlist_id varchar(100) references playlist(Pl_id),
                                                        Video_name varchar(100),
                                                        Video_descrip text,
                                                        Published_date timestamp,
                                                        View_count bigint,
                                                        Like_count bigint,
                                                        Favorite_count bigint,
                                                        Comment_count int,
                                                        Video_duration interval,
                                                        Thumbnail varchar(250),
                                                        Caption_status varchar(50)
                                                        )'''
        Cursor.execute(Create_T_Query)
        Connect_SQL.commit()
        
    except:
        print("Video table already created")


    # Get data from Mongodb and convert it into Data frame:
    Videolists=[]
    db=Client["Youtube_project1"]
    collection1=db["Youtube_channel_details"]

    for vid_data in collection1.find({},{"_id":0,"Video_details":1}):
        for ind in range(len(vid_data["Video_details"])):
            Videolists.append(vid_data["Video_details"][ind])
    df2=pd.DataFrame(Videolists)
    pprint(df2)

    # Insert values to Mysql table:
    for index,row in df2.iterrows():
        print(index,row)
        Insert_query='''insert into videos (Video_id,
                                                Playlist_id,
                                                Video_name,
                                                Video_descrip,
                                                Published_date,
                                                View_count,
                                                Like_count,
                                                Favorite_count,
                                                Comment_count,
                                                Video_duration,
                                                Thumbnail,
                                                Caption_status
                                                )
                                                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                                        
        values=(row['Video_id'],
                row['Playlist_id'],
                row['Video_name'],
                row['Video_descrip'],
                row['Published_date'],
                row['View_count'],
                row['Like_count'],
                row['Favorite_count'],
                row['Comment_count'],
                row['Video_duration'],
                row['Thumbnail'],
                row['Caption_status']
                )
        
        try:
            Cursor.execute(Insert_query,values)
            Connect_SQL.commit()
            
        except:
            print("Video details are already inserted")
            
    return "Video table is created in SQL"
#InsertSQL_videos=Create_sqltable_videos()


# Load data into Sql: # 4 comment Table
def Create_sqltable_comments():
    
    # SQL server connection:
    Connect_SQL, Cursor=Connect_SQL_server()

    # Delete sql table if exists:
    Drop_query='''drop table if exists comments cascade'''
    Cursor.execute(Drop_query)
    Connect_SQL.commit()

    # SQL Table creation:  
    try:   
        Create_T_Query='''create table if not exists comments (
                                                                Comment_id varchar(100) primary key,
                                                                Video_id varchar(100),
                                                                Comment_text text,
                                                                Comment_author varchar(100),
                                                                Comment_published_date timestamp
                                                                )'''
        
        Cursor.execute(Create_T_Query)
        Connect_SQL.commit()
        
    except:
        print("Comments table already created")


    # Get data from Mongodb and convert it into Data frame:
    Comment_lists=[]
    db=Client["Youtube_project1"]
    collection1=db["Youtube_channel_details"]

    for cmt_data in collection1.find({},{"_id":0,"Commend_details":1}):
        for ind in range(len(cmt_data["Commend_details"])):
            Comment_lists.append(cmt_data["Commend_details"][ind])
    df3=pd.DataFrame(Comment_lists)
    pprint(df3)

    # Insert values to Mysql table:
    for index,row in df3.iterrows():
        print(index,row)
        Insert_query='''insert into comments(Comment_id,
                                            Video_id,
                                            Comment_text,
                                            Comment_author,
                                            Comment_published_date
                                            )
                                            values(%s,%s,%s,%s,%s)'''
                                        
        values=(row['Comment_id'],
                row['Video_id'],
                row['Comment_text'],
                row['Comment_author'],
                row['Comment_published_date']
                )
        
        try:
            Cursor.execute(Insert_query,values)
            Connect_SQL.commit()
            
        except:
            print("Comment details are already inserted")
            
    return "Comments table is created in SQL"
#InsertSQL_comments=Create_sqltable_comments()


# Create all SQL Tables:
def Create_allSQL_tables():
    Create_sqltable_channels()
    Create_sqltable_playlists()
    Create_sqltable_videos()
    Create_sqltable_comments()

    return "All SQL tables are created"
#SQL_tables=Create_allSQL_tables()    


# Show SQL Channel Table:
def Show_SQLtab_Channels():
    
    Connect_SQL, Cursor=Connect_SQL_server()
    try:   
        Show_Tab_Query='''select * from channels'''
        Cursor.execute(Show_Tab_Query)
        Tab=Cursor.fetchall()
        dft=pd.DataFrame(Tab, columns=["Channel Id", "Channel Name", "Subscribers", 
                                    "Views", "Total Videos", "Channel Description", "Upload Id"])
        
    except:
        print("Error try again")
        
    return dft


# Show SQL Playlist Table:
def Show_SQLtab_Playlists():
    
    Connect_SQL, Cursor=Connect_SQL_server()    
    try:   
        Show_Tab_Query='''select * from playlist'''
        Cursor.execute(Show_Tab_Query)
        Tab=Cursor.fetchall()
        dft=pd.DataFrame(Tab, columns=["Playlist Id", "Channel Id", "Playlist Name","Video Count"])
        
    except:
        print("Error try again")
        
    return dft


# Show SQL Video Table:
def Show_SQLtab_Videos():
    
    Connect_SQL, Cursor=Connect_SQL_server()
    try:   
        Show_Tab_Query='''select * from videos'''
        Cursor.execute(Show_Tab_Query)
        Tab=Cursor.fetchall()
        dft=pd.DataFrame(Tab, columns=["Video Id","Playlist Id","Video Name", "Video Description",
                                    "Published Date","View Count","Like Count","Favorite Count",
                                    "Comment Count","Video Duration","Thumbnail","Caption Status"])
        
    except:
        print("Error try again")
        
    return dft


# Show SQL Comment Table:
def Show_SQLtab_Comments():
    
    Connect_SQL, Cursor=Connect_SQL_server()
    try:   
        Show_Tab_Query='''select * from comments'''
        Cursor.execute(Show_Tab_Query)
        Tab=Cursor.fetchall()
        dft=pd.DataFrame(Tab, columns=["Comment Id", "Video Id", "Comment Text",
                                    "Comment Author","Comment Published Date"])
        
    except:
        print("Error try again")
        
    return dft


# Get All Existing Channel Ids list from MongoDB:
def Getall_MDBExisting_ChannelsIds():
    
    Existing_Channels_Ids=[]
    db=Client["Youtube_project1"]
    collection1=db["Youtube_channel_details"]
    for ch_data in collection1.find({},{"_id":0,"Channel_details":1}):
        Existing_Channels_Ids.append(ch_data["Channel_details"]["Ch_id"])
    
    return Existing_Channels_Ids
#ExChannels_Ids=Getall_MDBExisting_ChannelsIds()


# Show All Existing Channel Ids & Names list from MongoDB:
def ShowEx_MDB_ChIdsNames():
    
    ExMDB_Channels_Ids=[]
    ExMDB_Channels_Names=[]
    db=Client["Youtube_project1"]
    collection1=db["Youtube_channel_details"]
    for ch_data in collection1.find({},{"_id":0,"Channel_details":1}):
        ExMDB_Channels_Ids.append(ch_data["Channel_details"]["Ch_id"])
        ExMDB_Channels_Names.append(ch_data["Channel_details"]["Ch_name"])
        
    dfCIN=pd.DataFrame({"Channel Id":ExMDB_Channels_Ids, "Channel Name":ExMDB_Channels_Names})
    dfCIN.reset_index(drop=True, inplace=True)
    dfCIN.index +=1
    
    return dfCIN
#ExMDB_ChIdName_Table=ShowEx_MDB_ChIdsNames()


# Delete MongoDB Collections
def Drop_MongoDB_Collections():
    try:
        Client=pymongo.MongoClient("mongodb+srv://Iyappan:iyappanmdb@cluster0.578ym4w.mongodb.net/?retryWrites=true&w=majority")
        db=Client["Youtube_project1"]
        Collections=db.list_collection_names()
        for collection_name in Collections:
            if collection_name=="Youtube_channel_details":
                db[collection_name].drop()
        Status="Success"
        
    except:
        Status="Failed"
        
    return Status

# Streamlit:

Op="HOME"
Op1="STORE DATA TO MONGODB" 
Op2="LOAD DATA INTO SQL"
Op3="DATA ANALYSIS & REPORTS"

if "User_Ch_idlist" not in st.session_state:
    st.session_state.User_Ch_idlist = []
    

CN1, CI1="Hobby Explorer Tamil", "UCYqXh1HzJSYYYmbaoK4veDw"
CN2, CI2="Mr. GK", "UC5cY198GU1MQMIPJgMkCJ_Q"
CN3, CI3="Science With Sam - அறிவியல் அறிவோம்", "UChGd9JY4yMegY6PxqpBjpRA"
CN4, CI4="Chitti", "UC3EIT1VMZvCCBe_NZgXNv4A"
CN5, CI5="Kaizen English", "UC44aT4ek1daiUsw2o1XUxow"

Ch_names=[CN1, CN2, CN3, CN4, CN5]
Ch_ids=[CI1, CI2, CI3, CI4, CI5]


st.set_page_config(page_title='Streamlit page1', layout="wide")
st.header(":orange[Youtube Data Harvesting and Warehousing using MongoDB, SQL and Streamlit]")

Note1='''To get youtube channel id, Open youtube in desktop/laptop & search youtube channel name and open it's home page. 
Then right click cursor on the homepage anywhere & open "View page source" or (Ctrl+U). 
And find channel id by using (Ctrl+F) and search "?channel_id" in the page source.
And copy the channel id.'''

def stream_data():
    for word in Note1.split():
        yield word + " "
        time.sleep(0.04)

Tab=option_menu(menu_title=None, 
                options=[Op, Op1, Op2, Op3],
                icons=["house","arrow-right-square","arrow-right-square","arrow-right-square","arrow-right-square"],
                default_index=0,
                orientation="horizontal",
                styles={
                        "container": {"padding": "0!important", "background-color": "#47c1f5"},
                        "icon": {"color": "red", "font-size": "16px"},
                        "nav-link": {"font-size": "12px", "text-align": "center", "margin":"3px", "--hover-color": "#c263cf"},
                        "nav-link-selected": {"font-size": "12px", "background-color": "#130938"}
                        }
                )

col1, col2=st.columns([2,6])
with col1:
    container1=st.container(border=True)
    
    with container1:
        if Tab==Op:
            st.write("<h5 style='color: blue;'>Key Technologies and Skills:</h5>", unsafe_allow_html=True)
            st.write('''1. Python scripting
                        \n 2. YouTube API integration
                        \n 3. Extract Transform Load (ETL)                        
                        \n 4. MongoDB Atlas
                        \n 5. SQL - PostgreSQL
                        \n 6. Pandas
                        \n 7. Plotly
                        \n 8. Data Warehousing
                        \n 9. Data Analysis
                        \n 10. Data Visualization
                        \n 11. Relational Database Management System (RDBMS)
                        \n 12. Streamlit
                        ''')            
        
        if Tab==Op1:
            st.write("<h5 style='color: blue;'>Fetch data from YouTube & Store in MongoDB:</h5>", unsafe_allow_html=True)
            with st.container(border=True):
                
                User_Ch_id= st.text_input('Enter the youtube channel id:', max_chars=24, help="Ex: UCYqXh1HzJSYYYmbaoK4xxYz")
                st.caption("Enter channel id one by one. Minimum required 2 ids & max 10 ids.")
                Store_MongoDB_button=st.button("Fetch data & Store", type="primary")
                Placeholder=st.empty()           
                
                if Store_MongoDB_button:
                    LenofChId=len(User_Ch_id)
                    if LenofChId==24:
                        if User_Ch_id not in st.session_state.User_Ch_idlist:
                            Len_User_CidL=len(st.session_state.User_Ch_idlist)
                            if Len_User_CidL < 10: 
                                st.session_state.User_Ch_idlist.append(User_Ch_id)                           
                                ExChannels_list=Getall_MDBExisting_ChannelsIds()                       
                                if User_Ch_id not in ExChannels_list:
                                    InsertMongoDB_status=Get_channel_all_details(User_Ch_id)
                                    Placeholder.success(InsertMongoDB_status)
                                elif User_Ch_id in ExChannels_list:
                                    Placeholder.info("This channel id is already exist")
                            
                    else:
                        Placeholder.error("Enter a valid channel Id.")
            
            
        if Tab==Op2:
            st.write("<h5 style='color: blue;'>Migrate Data from MongoDB to SQL :</h5>", unsafe_allow_html=True)            
            
            MDB_ChId_list=Getall_MDBExisting_ChannelsIds()
            Df_Channel_Id=pd.DataFrame({"Channel ids":MDB_ChId_list})
            Df_Channel_Id.reset_index(drop=True, inplace=True)
            Df_Channel_Id.index +=1
            st.write(Df_Channel_Id)
            Migrate_to_SQL=st.button("Migrate to SQL", type="primary")
            if Migrate_to_SQL:
                SQL_tables=Create_allSQL_tables()
                st.info(SQL_tables)
        
        
with col2:
    container2 = st.container(border=True)
    with container2:
        if Tab==Op:
            with st.container(border=False):
                st.write("<h5 style='color: orange;'>1. Store Data to MongoDB:</h5>", unsafe_allow_html=True)
                st.write("<h6 style='color: blue;'>Fetch data from Youtube & stote to MongoDB:</h6>", unsafe_allow_html=True)
                st.write('''Users can input YouTube channel ID and click the "Fetch data & Store" button And repeat for second channel ID. 
                        \nThe application fetches data from the YouTube API for each channel ID provided.
                        \nThe fetched data is stored in MongoDB collections, including channel details, playlists, videos, and comments.        
                        ''')
                
                st.write(''':red[**Note:**]''')
                st.write_stream(stream_data)
                st.write("<h7 style='color: green;'>Sample Youtube Channel Ids:</h7>", unsafe_allow_html=True)  
                df=pd.DataFrame({"Channel Ids":Ch_ids})
                df.reset_index(drop=True, inplace=True)
                df.index +=1
                st.table(df)
                st.write("<h6 style='color: blue;'>MongoDB Collections:</h6>", unsafe_allow_html=True)
                st.write('''Click 'Show MongoDB Collections' button, To view your MongoDB Collections list.''')
                
            with st.container(border=False):
                st.write("<h5 style='color: orange;'>2. Load Data into SQL:</h5>", unsafe_allow_html=True)
                st.write("<h6 style='color: blue;'>Migrate Youtube Data from MongoDB to SQL:</h6>", unsafe_allow_html=True)
                st.write('''Users select the "Load Data into SQL" option. 
                        \nThe application retrieves existing YouTube channel IDs from MongoDB & migrate to corresponding SQL tables.
                        ''')
                st.write("<h6 style='color: blue;'>SQL Collections:</h6>", unsafe_allow_html=True)
                st.write('''To view SQL table, select any one table from the given options.''')
                
            with st.container(border=False):
                st.write("<h5 style='color: orange;'>3. Data Analysis and Report:</h5>", unsafe_allow_html=True)
                st.write("<h6 style='color: blue;'>View Reports in Table or Chart:</h6>", unsafe_allow_html=True)
                st.write('''Users can select from a list of predefined questions for data analysis.
                        \nThe application executes SQL queries based on the selected question.
                        \nResults are displayed in tabular format or visualized using charts, depending on the user's preference.
                        ''')
                st.write(''':red[**Note:**]''')
                st.write('''If you want to delete all your MongoDB data, Click 'Delete MongoDB Collections' button.
                        Then MongoDB will be empty.''')
                
        if Tab==Op1:
            st.write("<h5 style='color: blue;'>1. MongoDB Collections:</h5>", unsafe_allow_html=True)
            st.write('''Click 'Show MongoDB Collections' button, To view your MongoDB Collections list.''')              
            Show_chlistst_button=st.button("Show MongoDB Collections", type="primary")

            if Show_chlistst_button:
                ExMDB_ChIdName_Table=ShowEx_MDB_ChIdsNames()
                st.table(ExMDB_ChIdName_Table)           
                
        if Tab==Op2:
            st.write("<h5 style='color: blue;'>2. SQL Collections:</h5>", unsafe_allow_html=True)
            st.write('''To view SQL table, select any one table from the following options.''')
            Radio_button=st.radio("Select the Table:", ("Channels Table", "Playlists Table", "Videos Table", "Comments Table"), index=0)
            if Radio_button=="Channels Table":
                SQLtab_Channels=Show_SQLtab_Channels()
                st.write(SQLtab_Channels)
                
            elif Radio_button=="Playlists Table":
                SQLtab_Playlists=Show_SQLtab_Playlists()
                st.write(SQLtab_Playlists)
            
            elif Radio_button=="Videos Table":
                SQLtab_Videos=Show_SQLtab_Videos()
                st.write(SQLtab_Videos)

            elif Radio_button=="Comments Table":
                SQLtab_Comments=Show_SQLtab_Comments()
                st.write(SQLtab_Comments)
        
if Tab==Op3:
    container3 = st.container(border=True)
    with container3:
        st.write("<h5 style='color: blue;'>3. View Reports in Table or Chart:</h5>", unsafe_allow_html=True)
        st.write('''To view data analysis report, Select your question from the following dropdown list.''')

        Selected_Question=st.selectbox("Select Question:", 
                                    ("1. What are the names of all the videos & corresponding channels?",
                                    "2. Which channels have most number of videos & how many videos?",
                                    "3. What are the top 10 most viewed videos & respective channels?",
                                    "4. How many comments were made on each video & their video names?",
                                    "5. Which videos have the highest no. of likes & their channel names?",
                                    "6. What is the total number of likes for each video & video names?",
                                    "7. What is the total number of views for each channel & channel names?",
                                    "8. What are the names of all channels which published videos in the given year?",
                                    "9. What is the average duration of all videos in each channel & names?",
                                    "10. Which videos have the highest number of comments & channel names?"
                                    ), index=0)
        Connect_SQL, Cursor=Connect_SQL_server()
        if Selected_Question=="1. What are the names of all the videos & corresponding channels?":
            Qry1='''SELECT videos.Video_name, channels.Ch_name
                    FROM channels
                    INNER JOIN playlist ON channels.Ch_id = playlist.Ch_id
                    INNER JOIN videos ON playlist.Pl_id = videos.Playlist_id
                    GROUP BY videos.Video_name, channels.Ch_name
                    ORDER BY channels.Ch_name ASC'''
            Cursor.execute(Qry1)
            Connect_SQL.commit()
            Tab1=Cursor.fetchall()
            dfT=pd.DataFrame(Tab1, columns=["Video Name","Channel Name"])
            st.write(dfT)

        elif Selected_Question=="2. Which channels have most number of videos & how many videos?":
            Qry2='''SELECT channels.Ch_name, channels.total_videos
                    FROM channels
                    GROUP BY channels.Ch_name, channels.total_videos
                    ORDER BY channels.total_videos DESC'''
            Cursor.execute(Qry2)
            Connect_SQL.commit()
            Tab1=Cursor.fetchall()
            dfT=pd.DataFrame(Tab1, columns=["Channel Name","No. of Videos"])
            dfT.reset_index(drop=True, inplace=True)
            
            Select_View=st.radio("Select any one view:", ["Table View", "Chart View"], index=0)
            if Select_View=="Table View":
                st.write(dfT)
                
            if Select_View=="Chart View":
                fig = px.bar(dfT, x='Channel Name', y='No. of Videos', title='Bar Chart: Number of Videos per Channel')
                fig.update_layout(xaxis_title='Channel Name', yaxis_title='No. of Videos')
                st.plotly_chart(fig)
                        
        elif Selected_Question=="3. What are the top 10 most viewed videos & respective channels?":
            Qry3='''SELECT videos.video_name, videos.view_count, channels.Ch_name
                    FROM channels
                    INNER JOIN playlist ON channels.Ch_id = playlist.Ch_id
                    INNER JOIN videos ON playlist.Pl_id = videos.Playlist_id
                    ORDER BY videos.view_count DESC LIMIT 10'''
            Cursor.execute(Qry3)
            Connect_SQL.commit()
            Tab1=Cursor.fetchall()
            dfT=pd.DataFrame(Tab1, columns=["Video Name","No. of Views","Channel Name"])
            st.write(dfT)

        elif Selected_Question=="4. How many comments were made on each video & their video names?":
            Qry4='''SELECT videos.video_name, videos.comment_count
                    FROM videos
                    ORDER BY videos.comment_count DESC'''
            Cursor.execute(Qry4)
            Connect_SQL.commit()
            Tab1=Cursor.fetchall()
            dfT=pd.DataFrame(Tab1, columns=["Video Name","No. of Comments"])
            st.write(dfT)
            

        elif Selected_Question=="5. Which videos have the highest no. of likes & their channel names?":
            Qry5='''SELECT videos.video_name, videos.like_count, channels.ch_name
                    FROM channels
                    INNER JOIN playlist ON channels.Ch_id = playlist.Ch_id
                    INNER JOIN videos ON playlist.Pl_id = videos.Playlist_id
                    WHERE videos.like_count IS NOT NULL
                    ORDER BY videos.like_count DESC'''
            Cursor.execute(Qry5)
            Connect_SQL.commit()
            Tab1=Cursor.fetchall()
            dfT=pd.DataFrame(Tab1, columns=["Video Name","No. of Likes","Channel Name"])
            st.write(dfT)

        elif Selected_Question=="6. What is the total number of likes for each video & video names?":
            Qry6='''SELECT videos.video_name, videos.like_count
                    FROM videos
                    WHERE videos.like_count IS NOT NULL
                    ORDER BY videos.like_count DESC'''
            Cursor.execute(Qry6)
            Connect_SQL.commit()
            Tab1=Cursor.fetchall()
            dfT=pd.DataFrame(Tab1, columns=["Video Name","No. of Likes"])
            st.write(dfT)


        elif Selected_Question=="7. What is the total number of views for each channel & channel names?":
            Qry7='''SELECT channels.ch_name, channels.views
                    FROM channels
                    ORDER BY channels.views DESC'''
            Cursor.execute(Qry7)
            Connect_SQL.commit()
            Tab1=Cursor.fetchall()
            dfT=pd.DataFrame(Tab1, columns=["Channel Name","No. of Views"])

            Select_View=st.radio("Select any one view:", ["Table View", "Chart View"], index=0)
            if Select_View=="Table View":
                st.write(dfT)
                
            if Select_View=="Chart View":
                #fig = px.bar(dfT, x='Channel Name', y='No. of Views', title='Number of Views per Channel')
                #fig.update_layout(xaxis_title='Channel Name', yaxis_title='No. of Views')
                
                fig = px.pie(dfT, values="No. of Views", names='Channel Name', title='Pie Chart: Number of Views per Channel')
                st.plotly_chart(fig)

        elif Selected_Question=="8. What are the names of all channels which published videos in the given year?":
            GivenYear=st.text_input("Enter Year", max_chars=4, help="YYYY")
            if GivenYear:
                try:
                    Qry8='''SELECT DISTINCT channels.Ch_name, TO_CHAR(videos.published_date, 'YYYY') AS Year
                            FROM channels
                            INNER JOIN playlist ON channels.Ch_id = playlist.Ch_id
                            INNER JOIN videos ON playlist.Pl_id = videos.Playlist_id
                            WHERE extract(year from videos.published_date)=%s'''
                    
                    Cursor.execute(Qry8,[GivenYear])
                    Connect_SQL.commit()
                    Tab1=Cursor.fetchall()
                    dfT=pd.DataFrame(Tab1, columns=["Channel Name","Video Published Year"])
                except:
                    dfT="Enter a valied Year"
                st.write(dfT)
                    
        elif Selected_Question=="9. What is the average duration of all videos in each channel & names?":
            Qry9='''SELECT channels.Ch_name, AVG(videos.video_duration) AS Average_Video_Duration
                    FROM channels
                    INNER JOIN playlist ON channels.Ch_id = playlist.Ch_id
                    INNER JOIN videos ON playlist.Pl_id = videos.Playlist_id
                    GROUP BY channels.Ch_name'''
                    
            Cursor.execute(Qry9)
            Connect_SQL.commit()
            Tab1=Cursor.fetchall()
            dfT=pd.DataFrame(Tab1, columns=["Channel Name","Average Video Duration"])
            
            Select_View=st.radio("Select any one view:", ["Table View", "Chart View"], index=0)
            if Select_View=="Table View":
                st.write(dfT)
                
            if Select_View=="Chart View":
                #fig = px.bar(dfT, x='Channel Name', y='Average Video Duration', title='Average Video Duration per Channel')
                #fig.update_layout(xaxis_title='Channel Name', yaxis_title='Average Video Duration')
                fig = px.scatter(dfT, x='Channel Name', y='Average Video Duration', color='Average Video Duration', title='Scatter Plot: Average Video Duration')
                st.plotly_chart(fig)

        elif Selected_Question=="10. Which videos have the highest number of comments & channel names?":
            Qry10='''SELECT videos.video_name, videos.comment_count, channels.Ch_name
                    FROM channels
                    INNER JOIN playlist ON channels.Ch_id = playlist.Ch_id
                    INNER JOIN videos ON playlist.Pl_id = videos.Playlist_id
                    WHERE videos.comment_count IS NOT NULL
                    ORDER BY videos.comment_count DESC'''
            Cursor.execute(Qry10)
            Connect_SQL.commit()
            Tab1=Cursor.fetchall()
            dfT=pd.DataFrame(Tab1, columns=["Video Name","Comment Count","Channel Name"])
            st.write(dfT)
            
        if st.button("Delete MongoDB Collections", type="secondary"):
            st.write("Are you sure want to delete all MongoDB data?. If yes, MongoDB will be empty.")
            if st.button("Yes"):
                Drop_Status=Drop_MongoDB_Collections()
                st.status(Drop_Status)
            if st.button("Cancel"):
                st.status("Cancelled")







