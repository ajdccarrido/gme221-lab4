# Laboratory Exercise 4 - Spatial Statistics: Spatial Autocorrelation and Cluster Detection

In this laboratory, the focus shifts toward spatial statistical analysis. Instead of asking how geometry is constructed, we now ask: 

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

The following GeoJSON files contain the Local Moran’s I spatial cluster results generated using different spatial weights methods and attribute variables. 

To reproduce these outputs, uncomment and modify the parameter for `w` `(Line 29-31 of server/analysis.py)`

- `contiguity_spatial_clusters (ass_ass_va).geojson`
- `contiguity_spatial_clusters (ass_market).geojson`
- `distance_weights_spatial_clusters (ass_ass_va).geojson`
- `distance_weights_spatial_clusters (ass_market).geojson`
- `knn_spatial_clusters (ass_ass_va).geojson`
- `knn_spatial_clusters (ass_market).geojson`

The QGIS project file contains the generated spatial cluster outputs with the corresponding symbology and visualization settings.

- `Lab4.qgz`

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

K-nearest neighbors (KNN) identifies neighbors based on proximity. For each parcel centroid, the method selects the `k` closest parcels as neighbors, where `k` is the parameter specified by the user.

Distance-based weights identify neighbors that fall within a specified distance threshold from a parcel centroid. A parcel is considered a neighbor if it lies within that distance.

Because each method defines neighbors differently, the resulting spatial graph can vary in structure and connectivity.

**3. Modify the parameter of one method.** 
**Examples:**
- increase K in KNN 
- increase the distance threshold in distance-based weights 

**What changes do you observe in the connectivity of the spatial graph?**

Increasing `k` in the KNN method increases the number of neighbors connected to each parcel centroid. For example, when `k = 4`, each parcel is connected to its four nearest neighbors; when `k = 5`, it connects to five neighbors.

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

### Reflection - Global Autocorrelation

**1. What does positive Moran’s I indicate?**

A positive Moran’s I indicates spatial clustering, meaning that areas with similar values (high–high or low–low) tend to occur near each other.

The Global Moran's I of the different spatial weights methods are shown below: 

#### Based on ass_ass_va
- Contiguity Weights: `0.3174760337303677`
- KNN (k=4): `0.18237132979784632`
- Distance Weights (20 m): `0.06794511037172285`

#### Based on ass_market
- Contiguity Weights: `0.2660243420175595`
- KNN (k=4): `0.1364143115453384`
- Distance Weights (20 m): `0.06001617825009126`

Among the three methods, `contiguity weights` produced the highest Moran’s I values, indicating stronger spatial clustering. KNN also shows clustering but at a weaker level. Distance-based weights produced the lowest values, suggesting a weaker spatial pattern that is closer to random.

**2. Why is the p-value required for interpretation?**

The p-value determines whether the observed Moran’s I is statistically significant or could have occurred by random chance.

#### Based on ass_ass_va
- Contiguity Weights: `0.001`
- KNN: `0.001`
- Distance Weights: `0.028`

#### Based on ass_market
- Contiguity Weights: `0.001`
- KNN: `0.001`
- Distance Weights: `0.012`

Since all p-values are below the common significance level (e.g., 0.05), the results indicate that the observed spatial clustering is statistically significant and unlikely to be random.

**3. What would Moran’s I near zero suggest?**

A value near zero suggests a random spatial pattern, where the distribution of values does not show meaningful clustering or dispersion across space.

**4. What is the role of the attribute in computing Moran’s I? Why the choice of attribute (e.g., ass_ass_va vs ass_market) matters.**

The attribute variable provides the values being compared across spatial units. Moran’s I measures whether similar attribute values occur near each other in space.

The choice of attribute matters because different variables may have different spatial distributions. For example, assessed values (`ass_ass_va`) and market values (`ass_market`) may reflect different economic or spatial patterns, which can affect the strength of spatial autocorrelation.

**5. How the spatial autocorrelation result might change when a different attribute is analyzed.**

Spatial autocorrelation results may vary depending on the attribute analyzed. If an attribute shows strong geographic clustering, Moran’s I will be higher. If the attribute values are more evenly distributed or random across space, the Moran’s I value will be lower. Therefore, different attributes can produce different levels of spatial autocorrelation.

**6. Why Moran’s I requires both:**
- a spatial weights matrix, and 
- an attribute variable. 

Moran’s I requires both components because they represent two key aspects of spatial analysis. The spatial weights matrix defines the neighborhood structure, indicating which spatial units influence each other. The attribute variable provides the values being compared across those spatial units. They allow the analysis to measure whether similar attribute values are spatially clustered according to the defined neighborhood relationships.

### Reflection - Interpreting Local Spatial Autocorrelation

**1. What is the difference between Global Moran’s I and Local Moran’s I? Explain how each statistic describes spatial autocorrelation at different spatial scales.**

Global Moran’s I measures overall spatial autocorrelation across the entire dataset, indicating whether similar values tend to cluster together or disperse across the study area. It provides a single summary statistic describing the general spatial pattern.

Local Moran’s I, in contrast, identifies specific locations where clustering occurs. It evaluates spatial autocorrelation at the level of the minimum mapping unit (MMU), which in this case is the parcel. This allows the detection of local clusters such as hotspots, coldspots, and spatial outliers.

**2. How are hotspots and coldspots identified using Local Moran’s I? Explain how the values of the statistic and the p-value determine whether a parcel belongs to a cluster.**

Hotspots and coldspots are identified based on the sign of the Local Moran’s I statistic and its statistical significance.

- A parcel with a **positive Local Moran’s I and a significant p-value `(p < 0.05)`** indicates that the parcel has a value similar to its neighbors. If the values are high, it forms a hotspot cluster (high–high).
- A parcel with a **negative Local Moran’s I and a significant p-value `(p < 0.05)`** indicates that the parcel has values different from its neighbors, which can indicate a coldspot or spatial outlier depending on the surrounding values.
- If the **`p-value ≥ 0.05`**, the parcel is considered not statistically significant, regardless of the Local Moran’s I value.

**3. Where do hotspots appear in your dataset? Describe the spatial location of clusters of high values. What geographic or urban factors might explain this pattern?**

Across different spatial weights and attributes, hotspot clusters consistently appear in the central portion of the dataset. These parcels likely represent areas with higher assessed or market values.

This pattern may be explained by urban factors such as the presence of commercial properties, higher accessibility, or proximity to services such as transportation, hospitals, and other urban amenities. Such factors typically increase land or property values, leading to clusters of high values.

**4. Where do coldspots appear in your dataset? Are there areas where low values cluster together? What spatial processes might explain these patterns?**

Using contiguity weights, coldspots appear on parcels located on the left side of the dataset for both `ass_ass_va` and `ass_market`. When using KNN and distance-based weights, coldspots tend to appear on the bottom-right portion of the dataset.

These clusters may represent areas with lower property values, which could be influenced by factors such as distance from commercial centers, limited accessibility, or differences in land use.

**5. Did you observe any spatial outliers? A spatial outlier occurs when a parcel has a value very different from its neighbors. Explain how such cases appear in the dataset.**

Yes, spatial outliers were observed. For example, the parcel with `gid = 699` appears as a hotspot surrounded by coldspots when using contiguity weights. Conversely, the parcel with `gid = 132` appears as a coldspot surrounded by hotspots.

These cases indicate parcels whose values differ significantly from those of their neighbors. One possible explanation is data inconsistency or estimation errors. For instance, a parcel’s assessed or market value may have been overestimated or underestimated relative to nearby parcels.

**6. How does changing the spatial weights method affect Local Moran’s I results? Repeat the analysis using another spatial weights method (e.g., KNN or distance). Do the hotspot locations change?**

Yes, changing the spatial weights method affects the Local Moran’s I results because each method defines neighborhood relationships differently.

For example, under contiguity weights, the large parcel with gid = 701 on the left side of the dataset shares boundaries with several parcels, making it a neighbor to many of them and influencing their classification. This results in several nearby parcels appearing as coldspots.

When using KNN or distance-based weights, the set of neighbors changes, which alters the Local Moran’s I values and the resulting cluster classifications. While hotspot and coldspot locations vary across methods, some parcels in the central area remain consistent hotspots, suggesting a stable spatial pattern.


**7. How does changing the attribute affect the spatial clusters? Run Local Moran’s I for:** 
- ass_ass_va 
- ass_market

**Compare the hotspot patterns. Why might these attributes produce different spatial clusters?**

Changing the attribute affects the spatial clusters because Local Moran’s I depends on the values of the variable being analyzed. When switching between ass_ass_va and ass_market, some parcels change classification—becoming hotspots, coldspots, or not statistically significant.

For both attributes, hotspots generally remain concentrated in the central parcels, although the number and exact locations vary depending on the spatial weights method used. Coldspots tend to appear in the bottom-right portion of the dataset.

In the context of this exercise, these differences occur because it is possible that the assessed values and market values reflect different valuation processes or economic conditions. These attributes also correspond to different values.