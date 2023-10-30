import logging

from confluent_kafka import Consumer, KafkaError
import csv
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Kafka broker connection details
bootstrap_servers = "kafka:9091"  # Use just one broker address

# Create a Kafka consumer instance
consumer = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
})

# Subscribe to the topic
topic = 'replication'
consumer.subscribe([topic])

# Open a CSV file named 'result.csv' for writing
csv_file = 'result.csv'
with open(csv_file, mode='w' , encoding='utf-8', newline='') as csv_file:
    fieldnames = ['Date', 'Message']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Consume and process messages
    logger.info('Started consuming')
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                logger.info('Reached end of partition')
            else:
                logger.info('Error: {}'.format(msg.error()))
        else:
            # Decode the message value as a string
            message = msg.value().decode('utf-8')
            logger.info(f'processing {message}')

            # Extract the date and file path
            date = message.split(' - ')[0]
            start_index = message.find("PFRO Error:") + len("PFRO Error:")
            end_index = message.rfind(",")
            extracted_string = message[start_index:end_index].strip()

            # Log the data separately
            logger.info("DATE_____________||____________FILE_PATHS")
            logger.info(f"{date}")
            logger.info(f"{extracted_string}")

            # Write the data to the CSV file
            writer.writerow({'Date': date, 'Message': extracted_string})



# Close the Kafka consumer
consumer.close()
