import geopandas as gpd
from sqlalchemy import create_engine
from spatial_weights import contiguity_weights, knn_weights, distance_weights
from visualization import visualize_neighbors, visualize_local_moran
from moran import calculate_global_morans_I
from esda.moran import Moran_Local
import os

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

# w = contiguity_weights(gdf)
# w = knn_weights(gdf)
w = distance_weights(gdf)

# print("Neighbors:", w.neighbors)

# visualize_neighbors(gdf, w)

# attribute = "ass_ass_va"
attribute = "ass_market"

# moran_I, p_value = calculate_global_morans_I(gdf, w, attribute)

# print("Global Moran's I:", moran_I)
# print("p-value:", p_value) 

local = Moran_Local(gdf[attribute], w)

gdf["local_I"] = local.Is
gdf["p_value"] = local.p_sim

gdf["cluster"] = "Not Significant"

gdf.loc[(gdf["local_I"] > 0) & (gdf["p_value"] < 0.05), "cluster"] = "Hotspot" 
gdf.loc[(gdf["local_I"] < 0) & (gdf["p_value"] < 0.05), "cluster"] = "Coldspot"

print(gdf.head())

# os.makedirs("output", exist_ok=True) 

gdf.to_file( 
    f"output/distance_weights_spatial_clusters ({attribute}).geojson", 
    driver="GeoJSON" 
)

# print("Saved: output/knn_spatial_clusters.geojson") 

# visualize_local_moran(gdf, attribute, "contiguity weights")
# visualize_local_moran(gdf, attribute, "knn weights")
visualize_local_moran(gdf, attribute, "distance weights")