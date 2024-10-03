import altair as alt
import pandas as pd
import streamlit as st
import BN_OPTION

option_dataframe = pd.DataFrame(columns=['CALL_OI','PUT_OI','CALL_COI','PUT_COI' ,'CALL_VOL',
            'PUT_VOL','CALL_TBQ','CALL_TSQ','PUT_TBQ','PUT_TSQ',])
request_index = pd.DataFrame(columns=['key','index','indexSymbol',
'last','variation','percentChange','open','high','low','previousClose','yearHigh',
'yearLow','indicativeClose','pe','pb','dy','declines','advances','unchanged'])
max_df =  pd.DataFrame(columns=['max_CS','max_CB','max_CT','max_CTOI','max_COI','max_CCOI','STP',
                                'max_PCOI','max_POI','max_PTOI','max_PT','max_PB','max_PS'])
max_df_2 = pd.DataFrame(columns=['max_CS','max_CB','max_CBIDQ','max_CASKQ','max_CT','max_CTOI','max_COI','max_CCOI','STP',
                                'max_PCOI','max_POI','max_PTOI','max_PT','max_PBIDQ','max_PASKQ','max_PB','max_PS'])



# Show the page title and description.
st.set_page_config(page_title="Movies dataset", page_icon="🎬")
st.title(" banknifty  dataset")
st.write(
    """
    This app visualizes data from [The NSE (BN)](https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY).
    It shows data of today !
    """
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df =  BN_OPTION.run_main(option_dataframe,max_df,max_df_2,request_index)[0]
    return df


df = load_data()

# Show a multiselect widget with the genres using `st.multiselect`.
# genres = st.multiselect(
#     "Genres",
#     df.genre.unique(),
#     ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"],
# )

# Show a slider widget with the years using `st.slider`.
# years = st.slider("Years", 1986, 2006, (2000, 2016))

# Filter the dataframe based on the widget input and reshape it.
# df_filtered = df[(df["genre"].isin(genres)) & (df["year"].between(years[0], years[1]))]
# df_reshaped = df_filtered.pivot_table(
#     index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0
# )
df_reshaped = df

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_reshaped,
    use_container_width=True,
    # column_config={"year": st.column_config.TextColumn("Year")},
)

# # Display the data as an Altair chart using `st.altair_chart`.
# df_chart = pd.melt(
#     df_reshaped.reset_index(), id_vars="year", var_name="genre", value_name="gross"
# )
# chart = (
#     alt.Chart(df_chart)
#     .mark_line()
#     .encode(
#         x=alt.X("year:N", title="Year"),
#         y=alt.Y("gross:Q", title="Gross earnings ($)"),
#         color="genre:N",
#     )
#     .properties(height=320)
# )
# st.altair_chart(chart, use_container_width=True)
