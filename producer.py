import random
from confluent_kafka import Producer

# Kafka broker connection details
bootstrap_servers = "kafka:9091,kafka-1:9092,kafka-2:9093"

# Create a producer instance
p = Producer({'bootstrap.servers': bootstrap_servers})

# Define the topic you want to produce messages to
topic = 'replication'

# Read log data from the Windows log file
log_file_path = 'PFRO.log'

# Define a list of keys
keys = ['key1', 'key2', 'key3']

# Open the log file and send each line as a message with a random key
with open(log_file_path, 'r') as log_file:
    for line in log_file:
        key = random.choice(keys)  # Randomly select a key from the list
        message = line.strip()
        p.produce(topic, key=key, value=message)
        print("Message with key '{}' successfully sent: {}".format(key, message))

# Flush the producer to ensure the messages are delivered
p.flush()
