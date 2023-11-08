def add_number(a,b):
    return a+b

'''
Aim: Installation of Docker, docker-Hadoop, Hive, mahout and Pig
(Additional requirements install wsl for windows)
Step 1 = Clone the Hadoop repo
git clone https://github.com/big-data-europe/docker-hadoop

Step 2 = Install Docker Desktop

Step 3 = Open the cloned directory docker-hadoop and open cmd
docker-compose up -d

Step 4 = Check all the running containers
docker container ls

check here = http://localhost:9870 or 50070

Step 5 = Get into namenode

docker exec -it namenode /bin/bash
#cd /tmp
#mkdir input
#echo "Hello World">input/f1.txt
#echo "Hello Docker">input/f2.txt
#hadoop fs -mkdir -p input
#hdfs dfs -put ./input/* input
#exit

Step 6 = Download the jar files from
https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-mapreduce-examples/2.7.1/hadoop-mapreduce-examples-2.7.1-sources.jar
and paste it in docker-hadoop folder

Step 6 = Check the namenode container id

Step 7 = .\hadoop-mapreduce-examples-2.7.1-sources.jar b69db6e8545d c:/tmp

Step 8 = docker cp hadoop-mapreduce-examples-2.7.1-sources.jar namenode:/tmp

Step 9
docker exec -it namenode /bin/bash
#cd /tmp
#hadoop jar hadoop-mapreduce-examples-2.7.1-sources.jar org.apache.hadoop.examples.WordCount input output

Check the output
#hdfs dfs -cat output/part-r-00000

INSTALLATION OF MAHOUT

go into docker-hadoop folder

docker pull apache/mahout-zeppelin:14.1
docker run -p 8080:8080 --rm --name whatever apache/mahout-zeppelin:14.1
Open the browser
http://localhost:8080

INSTALLATION OF HIVE

docker pull apache/hive:4.0.0-alpha-2
docker run -d -p 10000:10000 -p 10002:10002 --env SERVICE_NAME=hiveserver2 --name hive4 apache/hive:4.0.0-alpha-2
docker exec -it hive4 beeline -u 'jdbc:hive2://0.0.0.0:10000/'
----------------------------------------------------------------
*-*-*-*-*-*-PERFORM DATA CLEANING AND DO MAPREDUCE-*-*-*-*-*-*-*
----------------------------------------------------------------
import csv
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')

def clean_text(text):
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', cleaned_text)
    return cleaned_text.strip()

def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in text.split()]
    return ' '.join(lemmatized_words)

csv_file = 'spam.csv'

cleaned_reviews = []

with open(csv_file, 'r', encoding='latin-1') as file:
    reader = csv.reader(file)
    header = next(reader)
    for row in reader:
        review = row[0]
        cleaned_review = clean_text(review)
        lemmatized_review = lemmatize_text(cleaned_review)
        cleaned_reviews.append([lemmatized_review])

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(cleaned_reviews)


docker-compose up -d

docker exec -it namenode /bin/bash
#cd tmp
#mkdir message1
#exit

docker container ls

docker cp hadoop-mapreduce-examples-2.7.1-sources.jar namenode:/tmp

docker cp C:/Users/Practicals/spam.csv namenode:/tmp/message1

docker exec -it namenode /bin/bash

#hadoop fs -mkdir -p sss_message

#hdfs dfs -put ./tmp/message1/* sss_message
cd /tmp

hadoop jar hadoop-mapreduce-examples-2.7.1-sources.jar org.apache.hadoop.examples.WordCount sss_message final_outs

hdfs dfs -cat final_outs/part-r-00000

--------------------------------------------------
*-*-*-*-*-*-KMEANS CLUSTERING-*-*-*-*-*-*-*
-----------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris()
X = iris.data
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)

print(df.describe())

n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(X)

cluster_centers = kmeans.cluster_centers_
cluster_labels = kmeans.labels_

plt.scatter(X[:, 0], X[:, 1], c=cluster_labels, cmap='viridis')
plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1,], s=100, c='red', label='Cluster Centers')
plt.title("K-Means Clustering on Iris Dataset")
plt.legend()
plt.show()


-------
Using R
-------
install.packages(“factoextra”)
install.packages(“cluster”)


library("cluster")
library("factoextra")

wines <- read.csv("C:\\Users\\Desktop\\wines.csv")
summary(wines)
str(wines)

winescale <- as.data.frame(scale(wines))
head(winescale)


set.seed(95)
wines_k2 <- kmeans(winescale,centers = 3, nstart = 20)
print(wines_k2)
fviz_cluster(wines_k2, data = winescale)

wines[wines_k2$cluster == 1,]
wines[wines_k2$cluster == 2,]
wines[wines_k2$cluster == 3,]

------------------------------------------------------------
*-*-*-*-*-*Extract Data and Load in Hadoop-*-*-*-*-*-*-*
------------------------------------------------------------
the csv should be in docker-hadoop


docker-compose up -d

docker exec -it namenode bash

#hdfs dfs -mkdir -p /user/root1
#exit

docker cp .\hadoop-mapreduce-examples-2.7.1-sources.jar namenode:/tmp
docker cp .\custom_dataset_csv.csv namenode:/tmp

Get in the namenode container again
docker exec -it namenode bash

#hdfs dfs -mkdir /user/root/input11
# cd tmp
#hdfs dfs -put custom_dataset_csv.csv /user/root/input11

#hadoop jar hadoop-mapreduce-examples-2.7.1-sources.jar org.apache.hadoop.examples.WordCount input11 output11

hdfs dfs -cat /user/root/output11/*


'''