# Rabbit MQ Examples in Python

<p align="left">
    <a href="https://www.rabbitmq.com/">
        <img src="https://img.shields.io/badge/RabbitMQ-FF6600?logo=rabbitmq&logoColor=white&style=flat" alt="RabbitMQ Badge"/>
    </a>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=flat" alt="Python Badge"/>
    </a>
    <a href="https://wiki.python.org/moin/TkInter">
        <img src="https://img.shields.io/badge/Tkinter-FFB000?logo=python&logoColor=white&style=flat" alt="Tkinter Badge"/>
    </a>
</p>

RabbitMQ is a popular open-source message broker that enables applications to communicate with each other using messages, following the Advanced Message Queuing Protocol (AMQP). It is widely used for building scalable and distributed systems, allowing for reliable message delivery, decoupling of application components, and asynchronous processing. With Python, you can interact with RabbitMQ using libraries such as `pika` to send and receive messages between producers and consumers.

This app illustrates integration of RabbitMQ in Python using the Pika library. 

### Advanced Message Queuing Protocol

AMQP (Advanced Message Queuing Protocol) is an open-standard application layer protocol for message-oriented middleware. It defines a high-level, flexible, and robust way for applications to exchange messages asynchronously, reliably, and securely.

At its core, AMQP is about communication between software components where messages are sent to an intermediary (a message broker like RabbitMQ) rather than directly to recipients. This "store and forward" mechanism decouples senders (producers) from receivers (consumers), enhancing system flexibility, scalability, and resilience

AMQP supports various messaging patterns, including point-to-point, publish/subscribe, and request/reply. Its strength lies in its explicit definitions for features like message acknowledgments, persistent messages, and transaction support, ensuring reliable message delivery even in complex distributed systems. This makes AMQP a foundational protocol for building robust, scalable, and event-driven architectures.
