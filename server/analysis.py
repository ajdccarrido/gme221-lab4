import geopandas as gpd
from sqlalchemy import create_engine
from spatial_weights import contiguity_weights, knn_weights, distance_weights

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

w = contiguity_weights(gdf)

print("Neighbors:", w.neighbors)

