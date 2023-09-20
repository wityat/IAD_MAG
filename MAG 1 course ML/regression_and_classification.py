from pyarrow import csv

table = csv.read_csv("abalone.data")

print(table)
