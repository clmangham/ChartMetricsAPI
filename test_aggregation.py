import requests
import pandas as pd

# Test using local API (app.py - not dockerized)
# Endpoints 2 and 3 should return same rows even if sorting is a bit different

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        print(f"Failed to fetch data from {url}, status code {response.status_code}")
        return pd.DataFrame()

def prepare_dataframe(df, sort_keys):
    return df.sort_values(by=sort_keys).reset_index(drop=True)

def compare_dataframes(df1, df2, sort_keys):
    df1_sorted = prepare_dataframe(df1, sort_keys)
    df2_sorted = prepare_dataframe(df2, sort_keys)
    return df1_sorted.equals(df2_sorted)

if __name__ == '__main__':
    url_pandas = 'http://localhost:8000/summary/pandas'
    url_sql = 'http://localhost:8000/summary/sql'

    df_pd = fetch_data(url_pandas)
    df_sql = fetch_data(url_sql)


    if not df_pd.empty and not df_sql.empty:
        sort_keys = ['Observation_Type', 'Unit_Of_Measure']
        comparison = compare_dataframes(df_pd, df_sql, sort_keys)
        print("Are the dataframes (SQL processed and Pandas processed) equal?:", comparison)
        if not comparison:
            diff_pd = pd.merge(df_pd, df_sql, indicator=True, how='outer').query('_merge == "left_only"').drop('_merge', axis=1)
            diff_sql = pd.merge(df_pd, df_sql, indicator=True, how='outer').query('_merge == "right_only"').drop('_merge', axis=1)
            print("\nREVIEW PANDAS OUTPUT!!!")
            print(diff_pd)
            print("\nREVIEW SQL OUTPUT!!!")
            print(diff_sql)
    else:
        print("Data fetching failed, comparison not performed.")
