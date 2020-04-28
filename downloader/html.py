# %% ingest, clean
import pandas as pd
import numpy as np

def download_clean(url):
    """
    scrape from html source and return clean dataframe
    """
    weather_raw = pd.read_html(url)

    # unpack df list
    weather_1, weather_2 = weather_raw

    # strip double headers
    weather_1.columns = weather_1.columns.get_level_values(0)

    # merge
    weather = weather_1.merge(weather_2, on='Date August')

    # drop last 3 lines (aggregates)
    weather.drop(weather.tail(3).index, inplace=True)

    # concat year and month; to_datetime; resample to Days (remove time 00:00:00)
    weather['Date August'] = weather['Date August'].apply(lambda x: "2019-08-" + x)
    weather['Date August'] = pd.to_datetime(
        weather['Date August']).dt.to_period(freq="D")

    # duplicate column names
    cols = pd.Series(weather.columns)

    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [dup + '.' + str(i)
                                                        if i != 0 else dup for i in range(sum(cols == dup))]

    weather.columns = cols
    # %% feature extraction
    weather['Trace Rainfall'] = np.where(
        weather['Total Rainfall (mm)'] == 'Trace', 1, 0)
    # %% recast dtypes
    floats = ['Mean Pressure (hPa)', 'Air Temperature',
            'Mean Dew Point Temperature (deg. C)', 'Total Rainfall (mm)',
            'Total Bright Sunshine (hours)', 'Daily Global Solar Radiation (MJ/m2)',
            'Total Evaporation (mm)', 'Mean Wind Speed (km/h)']

    ints = ['Mean Relative Humidity (%)', 'Mean Amount of Cloud (%)',
            'Number of hours of Reduced Visibility# (hours)', 'Prevailing Wind Direction (degrees)']

    shit_features = list()  # catch shitty features e.g. 'trace' rainfall (mm)
    for column in ints:
        try:
            weather[column] = weather[column].astype(int, copy=False)
        except ValueError:
            shit_features.append(column)

    for column in floats:
        try:
            weather[column] = weather[column].replace('Trace', 0)
            weather[column] = weather[column].replace('-', 0)
            weather[column] = weather[column].astype(float, copy=False)
        except ValueError:
            shit_features.append(column)
    # %% reset index
    weather = weather.rename(columns={'Date August': 'Date'})
    weather.set_index('Date')
    # %% feature engineering
    weather['Mean Air Temperature'] = weather[['Air Temperature',
                                            'Air Temperature.1', 'Air Temperature.2']].mean(axis=1)
    return weather