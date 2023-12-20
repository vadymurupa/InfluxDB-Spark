import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, WriteOptions
from faker import Faker
import random
import os

token = os.environ.get("INFLUXDB_TOKEN")
org = "Test"
url = "http://localhost:8086"
bucket = "no"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=WriteOptions(batch_size=5000, flush_interval=10_000))

faker = Faker()

for _ in range(2000000):  # 2 million records
    point = (
        Point("measurement1")
        .tag("tagname1", faker.word())
        .field("field1", random.randint(1, 100))
        .time(faker.date_time_this_year())
    )
    write_api.write(bucket=bucket, org=org, record=point)

write_api.close()
client.close()

