# Laboratory Exercise 4 - Spatial Statistics: Spatial Autocorrelation and Cluster Detection

In this laboratory, the focus shifts toward spatial statistical analysis. Instead of asking how geometry 
is constructed, we now ask: 

***Are spatial values randomly distributed, clustered, or dispersed across space?***

This question is addressed through spatial autocorrelation statistics, particularly Moran’s I. 
By the end of this laboratory, you will: 

1. Retrieve spatial features from PostGIS into Python. 
2. Construct spatial weights matrices that define neighborhood relationships. 
3. Compute Global Moran’s I to measure overall spatial autocorrelation. 
4. Compute Local Moran’s I to identify spatial clusters. 
5. Detect hotspots and coldspots within parcel data. 
6. Visualize spatial statistical patterns using Python. 
7. Export spatial statistical results as GeoJSON for GIS visualization.

## How to Run Analysis.py

1. Install requirements.txt
2. Activate virtual environment
3. Run `analysis.py`

## Outputs Expected in output/

## Commit Milestones and Reflections

### Reflection - Interpreting the Neighborhood Structure
**1. How does the spatial weights graph represent neighborhood relationships? Explain how parcel centroids and connecting lines correspond to nodes and edges in a spatial network.**

The spatial weights graph represents neighborhood relationships as a network. Parcel centroids function as nodes, while the lines connecting them represent edges. Each edge indicates that two parcels are considered neighbors according to the chosen spatial weights method. In this way, the graph visualizes the spatial network that defines how parcels are related to one another.

**2. Change the spatial weights method and rerun the visualization. Compare the following methods:**
- contiguity weights 
- K-nearest neighbors (KNN) 
- distance-based weights

**How does the structure of the neighbor graph change?**

Contiguity weights identify neighbors based on shared boundaries between parcels. Parcels that touch each other are considered neighbors.

K-nearest neighbors (KNN) identifies neighbors based on proximity. For each parcel centroid, the method selects the k closest parcels as neighbors, where k is the parameter specified by the user.

Distance-based weights identify neighbors that fall within a specified distance threshold from a parcel centroid. A parcel is considered a neighbor if it lies within that distance.

Because each method defines neighbors differently, the resulting spatial graph can vary in structure and connectivity.

**3. Modify the parameter of one method.** 
**Examples:**
- increase K in KNN 
- increase the distance threshold in distance-based weights 

**What changes do you observe in the connectivity of the spatial graph?**

Increasing K in the KNN method increases the number of neighbors connected to each parcel centroid. For example, when k = 4, each parcel is connected to its four nearest neighbors; when k = 5, it connects to five neighbors.

Similarly, increasing the distance threshold in distance-based weights expands the search radius, which results in more parcels being identified as neighbors.

In both cases, increasing these parameters increases the connectivity of the spatial graph and produces a denser network of relationships.

**4. Does increasing K or distance create a denser spatial network? Explain how this might affect the strength of spatial autocorrelation.**

Yes. Increasing K in KNN or increasing the distance threshold results in more neighbors per parcel, which makes the spatial network denser. However, if these parameters become too large, most parcels will become neighbors with many others, even if they are far apart.

This can weaken or distort the measurement of spatial autocorrelation because the neighborhood structure becomes overly generalized. Parcels that are not spatially close may influence each other in the analysis, reducing the meaningful interpretation of spatial relationships.

**5. Which spatial weights method do you think best represents the spatial relationships of parcels in your dataset? Justify your answer conceptually.**

Contiguity weights best represent the spatial relationships of parcels because they are based on shared boundaries. In real-world land parcels, adjacent parcels directly influence each other through their physical proximity and boundary interaction. Therefore, defining neighbors based on contiguity reflects the most realistic spatial relationship.

For KNN and distance-based weights, selecting an appropriate number of neighbors or distance threshold requires additional analysis and should depend on the purpose of the study.

**6. Why is it important to visualize spatial weights before computing Moran’s I? What potential analytical mistakes could occur if the neighborhood structure is incorrect?**

Visualizing spatial weights helps ensure that the defined neighborhood structure accurately represents spatial relationships in the dataset. By examining the network of connections, we can verify whether the selected method and parameters are appropriate for the analysis.

If the neighborhood structure is incorrect, the results of Moran’s I may be misleading. For example, false hotspots or clusters may appear even when none exist, or real clusters may go undetected. Therefore, validating the spatial weights structure is an important step before conducting spatial autocorrelation analysis.