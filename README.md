# YouTube Data Harvesting and Warehousing using MongoDB, SQL, and Streamlit:

**Introduction:**

This YouTube project uses Python, MongoDB, SQL, and Streamlit to collect, store, and analyze YouTube data. With Python scripting and the YouTube API, it harvests data like channel details, videos, and comments. MongoDB and SQL databases store the data, while Streamlit provides a user-friendly interface for analysis. Pandas and Plotly aid in data exploration and visualization, enabling valuable insights from YouTube content.

**Installation:**

To run this project, you need to install the following packages:
```python
pip install google-api-python-client
pip install pymongo
pip install psycopg2
pip install pandas
pip install plotly
pip install streamlit
pip install streamlit_option_menu
```

**Tools and Libraries used:**

1. **Python:**

    Widely-used, high-level programming language known for simplicity, readability, extensive libraries, and versatility in web development, scientific computing, AI, and automation. Supports dynamic typing and automatic memory management.

2. **YouTube API:**

    The YouTube API provides access to YouTube's vast data, allowing developers to fetch channel details, playlists, videos, and comments. With the `googleapiclient` library, interactions with Google APIs, YouTube are simplified, streamlining data retrieval for analysis and processing.

3. **MongoDB:**

      MongoDB is a widely used NoSQL database storing data in JSON format documents, prized for scalability and ease of use. `pymongo` is its Python driver, facilitating interaction with MongoDB databases, enabling seamless data storage and retrieval in Python applications.

4. **PostgreSQL:**

      PostgreSQL is a robust relational database management system, used alongside MongoDB in this project for structured data storage. `Psycopg2` acts as the Python adapter for PostgreSQL, enabling efficient communication and data exchange between Python applications and PostgreSQL databases.

5. **Pandas:**

      Pandas is a powerful data manipulation and analysis library for Python. It provides data structures and functions for efficiently handling structured data, such as tabular data from databases.

6. **Plotly:**

      Plotly is a graphing library for Python that provides interactive and publication-quality plots. It offers various types of charts and visualizations for data exploration and presentation.

7. **Streamlit:**

      Streamlit is an open-source Python library for building web applications and interactive data dashboards with minimal code. It simplifies the process of creating and sharing data-driven applications, allowing users to focus on data analysis and visualization without needing expertise in web development.

**Project Workflow:**

1. **Initialization and Setup:**

        -	Install necessary Python libraries/modules like googleapiclient, pymongo, psycopg2, streamlit, pandas, plotly etc.

-	Obtain API keys for YouTube data access and configure them in the script.

-	Set up MongoDB and PostgreSQL databases where the fetched data will be stored.

2. **Data Retrieval from YouTube:**

-	Use the provided functions to fetch data from YouTube, such as channel details, playlist details, video details, and comments for each video.

-	This involves making API calls to the YouTube API using the `googleapiclient` library and processing the responses to extract relevant information.

3. **Data Storage in MongoDB:**

-	Store the fetched data into MongoDB collections. This includes channel details, playlists, videos, and comments.

-	The `pymongo` library is used to interact with MongoDB, where data is organized into collections.

4. **Data Processing and Storage in PostgreSQL:**

-	Process the fetched data and organize it into suitable formats for SQL tables.

-	Utilize the `psycopg2` library to establish a connection to the PostgreSQL database and create tables for storing channel details, playlist details, video details, and comments.

-	Insert the processed data into the corresponding SQL tables.

5. **User Interface Development:**

-	Develop a user interface using `streamlit` to interact with the data stored in the databases.

-	This may include features like displaying channel details, playlists, videos, comments, etc., in a user-friendly format.

6. **Data Analysis and Visualization:**

-	After storing the data in databases, perform any necessary data analysis or visualization using tools like `pandas`, `plotly`, etc.

-	Generate insights or visualize trends based on the retrieved YouTube data.

**How To Use:**

To use this project, follow these steps:

1.	Clone the repository: ```git clone https://github.com/iyappangithubacc/Youtube_project```
2.	Install the required packages: ```pip install -r requiretpackages.txt```
3.	Run the Streamlit app: ```streamlit run Youtubeproject.py```
4.	And access the web app in your browser at ```http://localhost:8501```

**Contact:**

**E-mail:** iyappandots@gmail.com

**Linkein:** http://www.linkedin.com/in/iyappandots 





