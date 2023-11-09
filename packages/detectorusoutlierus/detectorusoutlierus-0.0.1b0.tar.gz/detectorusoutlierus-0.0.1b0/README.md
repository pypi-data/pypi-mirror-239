<h1>detectorusoutlierus</h1>

<h4>Small package created for detecting outliers.</h4>

**Usage:**
* *<h5>install the package: from detectorusoutlierus import outliers as do</h5>*
* *"detect_outlier_mean_std"* - by mean and standard deviation. Takes column as a parameter
* *"detect_outlier_kvart"* - by kvartile. Takes column as a parameter
* *"detect_outlier_dbscan"* - with DBSCAN (clusterization). Takes two columns as a parameters
* *"detect_outlier_shovene"* - by Shovene method. Takes column as a parameter

**Example:**

from detectorusoutlierus import outliers as do

outlier_detector = do.Outline(df)

outliers_mean = outlier_detector.detect_outlier_mean_std('column_name')

outliers_mean