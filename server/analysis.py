import geopandas as gpd
from sqlalchemy import create_engine
from spatial_weights import contiguity_weights, knn_weights, distance_weights
from visualization import visualize_neighbors
from moran import calculate_global_morans_I

# Database connection parameters
host = "localhost"
port = "5432"
dbname = "gme221_exer4"
user = "ajdcc"
password = "gme221_db"

conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(conn_str)

sql_query = """
SELECT gid, ass_ass_va, ass_market, geom
FROM public.assessed_parcels;
"""

gdf = gpd.read_postgis(sql_query, engine, geom_col="geom")

# print(gdf.head())
# print("CRS:", gdf.crs)

w = distance_weights(gdf)

# print("Neighbors:", w.neighbors)

# visualize_neighbors(gdf, w)

attribute = "ass_market"

moran_I, p_value = calculate_global_morans_I(gdf, w, attribute)

print("Global Moran's I:", moran_I)
print("p-value:", p_value)