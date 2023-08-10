# OWRI Framework
outlier weightage real-time intersection ramework

**outlier weightage intersection model:**

<p align="center">
  <img src="docs/outlier_model.png" alt="Example image"/>
</p>


**Real-time outlier based updating strategy :**
<p align="center">
  <img src="docs/real_time_model.png" alt="Example image"/>
</p>





# GNN Networks  

Use the following link to generate training data for GNNs for the hague GNN_raw_data  - https://github.com/liyaguang/DCRNN

- Generate train, test and val data
- Generate distance based adjcency matrix


To run different GNN models follow - https://github.com/tsinghua-fib-lab/Traffic-Benchmark 

The below results are for 1 epoch with 70/20/10 split between train, test and validation datasets



===== \
**Results for 3 runs**

valid	MAE	RMSE	MAPE \
mean:	10.2460	13.5316	0.8379 \
std:	14.4900	19.1365	1.1849



test|horizon	MAE-mean	RMSE-mean	MAPE-mean	MAE-std	RMSE-std	MAPE-std 

3	10.1361	12.3946	1.0670	14.3346	17.5286	1.5089 \
6	9.4435	12.1124	0.9348	13.3551	17.1295	1.3221 \
9	9.1918	12.1480	0.8508	12.9992	17.1799	1.2032 \
12	9.2029	12.1316	0.8568	13.0149	17.1567	1.2117 
