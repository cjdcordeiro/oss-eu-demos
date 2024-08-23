#!/usr/bin/env python3

import argparse
import asyncio
import logging
import sys
import valkey.asyncio as valkey

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
STOPWORD = "STOP"


def parser():
    parser = argparse.ArgumentParser(description="Valkey ")
    parser.add_argument(
        "-p", "--port", type=int, required=True, help="Port number (e.g., 6379)."
    )
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help='There host where Valkey server is running. The default is "localhost"',
    )
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=["pub", "sub"],
        required=True,
        help='Type of the application, must be "sub" (subscriber) or "pub" (publisher).',
    )
    return parser.parse_args()


async def reader(channel: valkey.client.PubSub):
    while True:
        message = await channel.get_message(
            ignore_subscribe_messages=True, timeout=None
        )
        if message is not None:
            logging.info(f"(Reader) Message Received: {message['data'].decode()}")
            if message["data"].decode() == STOPWORD:
                logging.warning("(Reader) STOP")
                break


async def async_main():
    args = parser()
    r = valkey.Valkey(host="localhost", port=args.port, db=0)
    await r.ping()
    async with r.pubsub() as pubsub:
        if args.type == "sub":
            await pubsub.subscribe("channel:1")
            future = asyncio.create_task(reader(pubsub))
            await future
        else:
            while True:
                message = input("Message: ")
                await r.publish("channel:1", message)
                if message == "STOP":
                    logging.warning("Stopping the loop.")
                    break


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
