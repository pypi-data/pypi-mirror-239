# Copyright 2023 Aineko Authors
# SPDX-License-Identifier: Apache-2.0
"""A wrapper class that executes Docker CLI commands via subprocess."""
import subprocess


class KafkaCLIWrapper:
    """A utility class for interacting with Kafka using command-line tools.

    This class provides methods to consume messages from a
    Kafka topic using the Kafka console consumer.
    """

    @classmethod
    def consume_kafka_topic(cls, topic_name: str, from_beginning: bool) -> None:
        """Consume messages from a Kafka topic using the Kafka console consumer.

        Args:
            topic_name: The name of the Kafka topic to consume
            messages from.

            from_beginning: If True, start consuming from the
            beginning of the topic. If False, start consuming from
            the current offset.

        Raises:
            subprocess.CalledProcessError: If there is an error running
            the Kafka viewer.

        Example:
            To consume messages from a Kafka topic 'my-topic' from the beginning

            >>> KafkaCLIWrapper.consume_kafka_topic('my-topic', True)
        """
        if from_beginning:
            command = (
                "docker exec -it broker kafka-console-consumer"
                " --bootstrap-server localhost:9092 --topic"
                f" {topic_name} --from-beginning"
            )
        else:
            command = (
                "docker exec -it broker kafka-console-consumer"
                f" --bootstrap-server localhost:9092 --topic {topic_name}"
            )
        try:
            with subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # Line-buffered
                universal_newlines=True,
            ) as process:
                if process.stdout is not None:
                    for line in process.stdout:
                        print(line.strip())

            process.wait()
        except subprocess.CalledProcessError as ex:
            print(f"Error running Kafka viewer: {ex}")
            print(f"Command output: {ex.output}")
