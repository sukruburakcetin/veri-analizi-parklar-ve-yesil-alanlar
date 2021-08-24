import keplergl
import pandas as pd

# read csv
df = pd.read_csv('../../../Data/Non-GIS Data/cleaned/park_location_cleaned.csv')

# lat and lon to numeric, errors converted to nan
df['latitude'] = pd.to_numeric(df.latitude, errors='coerce')
df['longitude'] = pd.to_numeric(df.longitude, errors='coerce')

# drop rows with missing lat, lon, and intensity
df.dropna(subset=['latitude', 'longitude'], inplace=True)

kepler_map = keplergl.KeplerGl(height=1400)

kepler_map.add_data(data=df, name="institution_type_tr")

kepler_map.save_to_html(file_name='parklarveyesilalanlar_istanbul.html', read_only=True, center_map=True)
