# -*- coding: utf-8 -*-

import datetime
import time
from threading import Lock
from typing import List, Optional

from confluent_kafka import Message
from pip_services4_commons.errors import ConnectionException, InvalidStateException
from pip_services4_components.config import ConfigParams
from pip_services4_components.context import IContext, ContextResolver, Context
from pip_services4_components.refer import IUnreferenceable, IReferences, DependencyResolver
from pip_services4_components.run import IOpenable, ICleanable
from pip_services4_messaging.queues import MessageQueue, MessageEnvelope, IMessageReceiver, MessagingCapabilities
from pip_services4_observability.log import CompositeLogger

from pip_services4_kafka.connect.IKafkaMessageListener import IKafkaMessageListener
from pip_services4_kafka.connect.KafkaConnection import KafkaConnection


class KafkaMessageQueue(MessageQueue, IKafkaMessageListener, IUnreferenceable, IOpenable, ICleanable):
    """
    Message queue that sends and receives messages via Kafka message broker.

    Kafka is a popular light-weight protocol to communicate IoT devices.

    ### Configuration parameters ###
        - topic:                         name of Kafka topic to subscribe
        - group_id:                      (optional) consumer group id (default: default)
        - from_beginning:                (optional) restarts receiving messages from the beginning (default: false)
        - read_partitions:               (optional) number of partitions to be consumed concurrently (default: 1)
        - autocommit:                    (optional) turns on/off autocommit (default: true)
        - connection(s):
          - discovery_key:               (optional) a key to retrieve the connection from :class:`IDiscovery <pip_services4_components.connect.IDiscovery.IDiscovery>`
          - host:                        host name or IP address
          - port:                        port number
          - uri:                         resource URI or connection string with all parameters in it
        - credential(s):
          - store_key:                   (optional) a key to retrieve the credentials from :class:`ICredentialStore <pip_services4_components.auth.ICredentialStore.ICredentialStore>`
          - username:                    user name
          - password:                    user password
        - options:
          - num_partitions:       (optional) number of partitions of the created topic (default: 1)
          - replication_factor:   (optional) kafka replication factor of the topic (default: 1)
          - readable_partitions:      (optional) list of partition indexes to be read (default: all)
          - write_partition:      (optional) write partition index (default: uses the configured built-in partitioner)
          - autosubscribe:        (optional) true to automatically subscribe on option (default: false)
          - acks                  (optional) control the number of required acks: -1 - all, 0 - none, 1 - only leader (default: -1)
          - log_level:            (optional) log level 0 - None, 1 - Error, 2 - Warn, 3 - Info, 4 - Debug (default: 1)
          - connect_timeout:      (optional) number of milliseconds to connect to broker (default: 1000)
          - max_retries:          (optional) maximum retry attempts (default: 5)
          - retry_timeout:        (optional) number of milliseconds to wait on each reconnection attempt (default: 30000)
          - request_timeout:      (optional) number of milliseconds to wait on flushing messages (default: 30000)

    ### References ###
        - `*:logger:*:*:1.0`            (optional) :class:`ILogger <pip_services4_components.log.ILogger.ILogger>` components to pass log messages
        - `*:counters:*:*:1.0`          (optional) :class:`ICounters <pip_services4_components.count.ICounters.ICounters>` components to pass collected measurements
        - `*:discovery:*:*:1.0`         (optional) :class:`IDiscovery <pip_services4_components.connect.IDiscovery.IDiscovery>` services to resolve connection
        - `*:credential-store:*:*:1.0`  (optional) Credential stores to resolve credentials
        - `*:connection:kafka:*:1.0`    (optional) Shared connection to Kafka service

    Example:

    .. code-block:: python

        queue = KafkaMessageQueue("myqueue")
        queue.configure(ConfigParams.from_tuples(
            "topic", "mytopic",
            'connection.protocol', 'tcp',
            "connection.host", "localhost",
            "connection.port", 9092,
        ))

        queue.open("123")
        queue.send("123", MessageEnvelope(None, "mymessage", "ABC"))
        message = queue.receive("123", 10000)

        print(message)

        if message is not None:
            ...
            queue.complete(message)


    """
    __default_config = ConfigParams.from_tuples(
        "topic", None,
        "group_id", "default",
        "from_beginning", False,
        "read_partitions", 1,
        "autocommit", True,
        "options.autosubscribe", False,
        "options.acks", -1,
        "options.log_level", 1,
        "options.connect_timeout", 1000,
        "options.retry_timeout", 30000,
        "options.max_retries", 5,
        "options.request_timeout", 30000
    )

    def __init__(self, name: str = None):
        """
        Creates a new instance of the persistence component.

        :param name: (optional) a queue name.
        """
        super().__init__(name, MessagingCapabilities(False, True, True, True, True, False, True, False, True))

        self.__lock = Lock()

        self._config: ConfigParams = None
        self._references: IReferences = None
        self._opened: bool = None
        self._local_connection: bool = None

        # The dependency resolver.
        self._dependency_resolver: DependencyResolver = DependencyResolver(self.__default_config)

        # The logger.
        self._logger: CompositeLogger = CompositeLogger()

        # The Kafka connection component.
        self._connection: KafkaConnection = None

        self._topic: str = ''
        self._group_id: str = ''
        self._from_beginning: bool = False
        self._auto_commit: bool = True
        self._read_partitions: int = 1
        self._acks: int = -1
        self._auto_subscribe: bool = False
        self._subscribed: bool = False
        self._messages: List[MessageEnvelope] = []
        self._receiver: IMessageReceiver = None

    def configure(self, config: ConfigParams):
        """
        Configures object by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        config = config.set_defaults(self.__default_config)
        self._config = config

        self._dependency_resolver.configure(config)

        self._topic = config.get_as_string_with_default("topic", self._topic)
        self._group_id = config.get_as_string_with_default("group_id", self._group_id)
        self._from_beginning = config.get_as_boolean_with_default("from_beginning", self._from_beginning)
        self._read_partitions = config.get_as_integer_with_default("read_partitions", self._read_partitions)
        self._auto_commit = config.get_as_boolean_with_default("autocommit", self._auto_commit)
        self._auto_subscribe = config.get_as_boolean_with_default("options.autosubscribe", self._auto_subscribe)
        self._acks = config.get_as_integer_with_default("options.acks", self._acks)
        self._name = config.get_as_string_with_default('topic', self._name)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._references = references
        self._logger.set_references(references)

        # Get connection
        self._dependency_resolver.set_references(references)
        self._connection = self._dependency_resolver.get_one_optional('connection')
        # Or create a local one
        if self._connection is None:
            self._connection = self.__create_connection()
            self._local_connection = True
        else:
            self._local_connection = False

    def unset_references(self):
        """
        Unsets (clears) previously set references to dependent components.
        """
        self._connection = None

    def __create_connection(self) -> KafkaConnection:
        connection = KafkaConnection()

        if self._config:
            connection.configure(self._config)

        if self._references:
            connection.set_references(self._references)

        return connection

    def is_open(self) -> bool:
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self._opened

    def open(self, context: Optional[IContext]):
        """
        Opens the component.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self._opened:
            return

        if self._connection is None:
            self._connection = self.__create_connection()
            self._local_connection = True

        if self._local_connection:
            self._connection.open(context)

        if not self._connection.is_open():
            raise ConnectionException(
                context,
                "CONNECT_FAILED",
                "Kafka connection is not opened"
            )

        # create topic if it does not exist
        if self._get_topic() not in self._connection.read_queue_names():
            self._connection.create_queue(self._get_topic())

        # Subscribe right away
        if self._auto_subscribe:
            self._subscribe(context)

        self._opened = True

    def close(self, context: Optional[IContext]):
        """
        Closes component and frees used resources.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if not self._opened:
            return

        if self._connection is None:
            raise InvalidStateException(
                ContextResolver.get_trace_id(context),
                'NO_CONNECTION',
                'Kafka connection is missing'
            )

        if self._local_connection:
            self._connection.close(None)

        # Unsubscribe from the topic
        if self._subscribed:
            topic = self._get_topic()
            self._connection.unsubscribe(topic, self._group_id, self)

        self._subscribed = False
        with self.__lock:
            self._messages = []
            self._opened = False
            self._receiver = None

    def _get_topic(self) -> str:
        return self._topic if self._topic is not None and self._topic != '' else self.get_name()

    def _subscribe(self, context: Optional[IContext]):
        """
        Subscribe to the topic

        :param context: (optional) transaction id to trace execution through call chain.
        """
        if self._subscribed:
            return

        topic = self._get_topic()

        options = {
            'from_beginning': 'beginning' if self._from_beginning else None,
            'enable.auto.commit': self._auto_commit,
            # 'partitionsConsumedConcurrently': self._readable_partitions
        }

        self._connection.subscribe(topic, self._group_id, options, self)

        self._subscribed = True

    def _from_message(self, message: MessageEnvelope) -> Optional[dict]:
        if message is None:
            return

        msg = {
            'key': message.message_id,
            'value': message.get_message_as_string(),
            'headers': {
                'message_type': message.message_type,
                'trace_id': message.trace_id
            },
            'timestamp': int(datetime.datetime.now().timestamp() * 1000)
        }

        return msg

    def _to_message(self, msg: Message) -> Optional[MessageEnvelope]:
        if msg is None:
            return

        message_type = self.__get_header_by_key(msg.headers(), 'message_type')
        trace_id = self.__get_header_by_key(msg.headers(), 'trace_id')

        message = MessageEnvelope(Context.from_trace_id(trace_id), message_type, None)
        message.message_id = msg.key().decode('utf-8')
        message.sent_time = datetime.datetime.fromtimestamp(msg.timestamp()[1] / 1000)
        message.set_message_as_string(msg.value().decode('utf-8'))
        message.set_reference(msg)

        return message

    def __get_header_by_key(self, headers: list, key: str) -> Optional[str]:
        if headers is None:
            return

        for header in headers:
            k, v = header
            if k == key:
                return v.decode('utf-8')

    def on_message(self, topic: str, partition: int, message: Message):
        # Deserialize message
        message = self._to_message(message)
        if message is None:
            self._logger.error(None, None, "Failed to read received message")

        self._counters.increment_one("queue." + self.get_name() + ".received_messages")
        self._logger.debug(Context.from_trace_id(message.trace_id), "Received message %s via %s", message,
                           self.get_name())

        # Send message to receiver if its set or put it into the queue
        if self._receiver is not None:
            self.__send_message_to_receiver(self._receiver, message)
        else:
            with self.__lock:
                self._messages.append(message)

    def clear(self, context: Optional[IContext]):
        """
        Clears component state.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        with self.__lock:
            self._messages = []

    def read_message_count(self) -> int:
        """
        Reads the current number of messages in the queue to be delivered.

        :return: a number of messages in the queue.
        """
        with self.__lock:
            return len(self._messages)

    def peek(self, context: Optional[IContext]) -> MessageEnvelope:
        """
        Peeks a single incoming message from the queue without removing it.
        If there are no messages available in the queue it returns null.

        :param context: (optional) transaction id to trace execution through call chain.
        :return: a peeked message.
        """
        self._check_open(context)

        # Subscribe to topic if needed
        self._subscribe(None)

        # Peek a message from the top
        message = None

        with self.__lock:
            if len(self._messages) > 0:
                message = self._messages[0]

        if message is not None:
            self._logger.trace(Context.from_trace_id(message.trace_id), "Peeked message %s on %s", message,
                               self.get_name())

        return message

    def peek_batch(self, context: Optional[IContext], message_count: int) -> List[MessageEnvelope]:
        """
        Peeks multiple incoming messages from the queue without removing them.
        If there are no messages available in the queue it returns an empty list.

        :param context: (optional) transaction id to trace execution through call chain.
        :param message_count: a maximum number of messages to peek.
        :return: a list with peeked messages.
        """
        self._check_open(context)

        # Subscribe to topic if needed
        self._subscribe(None)

        # Peek a batch of messages
        with self.__lock:
            messages = self._messages[0:message_count]

        self._logger.trace(context, "Peeked message %s on %s", len(messages), self.get_name())

        return messages

    def receive(self, context: Optional[IContext], wait_timeout: int) -> MessageEnvelope:
        """
        Receives an incoming message and removes it from the queue.

        :param context: (optional) transaction id to trace execution through call chain.
        :param wait_timeout: a timeout in milliseconds to wait for a message to come.
        :return: a received message.
        """
        self._check_open(context)

        # Subscribe to topic if needed
        self._subscribe(None)

        # Peek a batch of messages
        message = None

        # Return message immediately if it exist
        with self.__lock:
            if len(self._messages) > 0:
                message = self._messages.pop(0)
                return message

        # Otherwise wait and return
        check_interval = 100
        elapsed_time = 0

        while True:
            test = self.is_open() and elapsed_time < wait_timeout and message is None
            if not test:
                break

            time.sleep(check_interval / 1000)
            with self.__lock:
                if len(self._messages) > 0:
                    message = self._messages.pop(0)
            elapsed_time += check_interval

        return message

    def send(self, context: Optional[IContext], envelop: MessageEnvelope):
        """
        Sends a message into the queue.

        :param context: (optional) transaction id to trace execution through call chain.
        :param envelop: a message envelop to be sent.
        """
        self._check_open(context)

        self._counters.increment_one("queue." + self.get_name() + ".sent_messages")
        self._logger.debug(Context.from_trace_id(envelop.trace_id), "Sent message %s via %s", envelop.to_string(),
                           self.to_string())

        msg = self._from_message(envelop)
        topic = self.get_name() or self._topic
        self._connection.publish(topic, [msg])

    def renew_lock(self, message: MessageEnvelope, lock_timeout: int):
        """
        Renews a lock on a message that makes it invisible from other receivers in the queue.
        This method is usually used to extend the message processing time.

        Important: This method is not supported by Kafka.

        :param message: a message to extend its lock.
        :param lock_timeout: a locking timeout in milliseconds.
        """
        # Not supported

    def complete(self, message: MessageEnvelope):
        """
        Permanently removes a message from the queue.
        This method is usually used to remove the message after successful processing.

        :param message: a message to remove.
        """
        # Check open status
        self._check_open(None)

        # Incomplete message shall have a reference
        msg = message.get_reference()

        # Skip on autocommit
        if self._auto_commit or msg is None or msg.get('partition') or msg.get('offset') is None:
            return

        # Commit the message offset so it won't come back
        topic = self._get_topic()

        self._connection.commit(topic, self._group_id, msg['partition'], msg['offset'], self)

    def abandon(self, message: MessageEnvelope):
        """
        Returnes message into the queue and makes it available for all subscribers to receive it again.
        This method is usually used to return a message which could not be processed at the moment
        to repeat the attempt. Messages that cause unrecoverable errors shall be removed permanently
        or/and send to dead letter queue.

        :param message: a message to return.
        """
        # Check open status
        self._check_open(None)

        # Incomplete message shall have a reference
        msg = message.get_reference()

        # Skip on autocommit
        if self._auto_commit or msg is None or msg.get('partition') or msg.get('offset') is None:
            return

        # Seek to the message offset so it will come back
        topic = self._get_topic()
        self._connection.seek(topic, self._group_id, msg['partition'], msg['offset'], self)

    def move_to_dead_letter(self, message: MessageEnvelope):
        """
        Permanently removes a message from the queue and sends it to dead letter queue.

        Important: This method is not supported by Kafka.

        :param message: a message to be removed.
        """
        # Not supported

    def __send_message_to_receiver(self, receiver: IMessageReceiver, message: MessageEnvelope):
        trace_id = None if message is None else message.trace_id
        if message is None or receiver is None:
            self._logger.warn(Context.from_trace_id(trace_id), "Kafka message was skipped.")
            return

        try:
            self._receiver.receive_message(message, self)
        except Exception as err:
            self._logger.error(Context.from_trace_id(trace_id), err, 'Failed to process the message')

    def listen(self, context: Optional[IContext], receiver: IMessageReceiver):
        """
        Listens for incoming messages and blocks the current thread until queue is closed.

        :param context: (optional) transaction id to trace execution through call chain.
        :param receiver: a receiver to receive incoming messages.
        """
        self._check_open(context)

        # Subscribe to topic if needed
        self._subscribe(context)

        self._logger.trace(context, "Started listening messages at %s", self.get_name())

        # Resend collected messages to receiver
        with self.__lock:
            while self.is_open() and len(self._messages) > 0:
                message = self._messages.pop(0)
                if message is not None:
                    self.__send_message_to_receiver(receiver, message)

        # Set the receiver
        if self.is_open():
            self._receiver = receiver

    def end_listen(self, context: Optional[IContext]):
        """
        Ends listening for incoming messages.
        When this method is call `listen` unblocks the thread and execution continues.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        with self.__lock:
            self._receiver = None
