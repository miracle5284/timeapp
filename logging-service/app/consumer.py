import asyncio
import json
import logging
import redis.asyncio as async_redis
from redis.exceptions import ConnectionError as RedisConnectionError, TimeoutError
from .config import REDIS_HOST, REDIS_PORT, LOG_STREAM
from .logdna_logger import send_log_to_logdna

logger = logging.getLogger(__name__)

async def get_redis_connection():
    try:
        redis_client = async_redis.Redis(
            host=REDIS_HOST, 
            port=REDIS_PORT, 
            decode_responses=True,
            socket_timeout=10,
            socket_connect_timeout=10,
            retry_on_timeout=True,
            health_check_interval=30
        )
        # Test the connection
        await redis_client.ping()
        logger.info("Successfully connected to Redis")
        return redis_client
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise

async def consume_logs():
    try:
        r = await get_redis_connection()
        last_id = "0-0"
        logger.info("Log consumer started. Waiting for logs...")

        while True:
            try:
                # XREAD is a list of (stream_name, [ (message_id, dict), ... ])
                response = await r.xread({LOG_STREAM: last_id}, count=10, block=5000)

                # If no new messages after 5s, xread returns an empty list []
                if not response:
                    await asyncio.sleep(1)
                    continue

                for stream_name, messages in response:
                    for message_id, message_data in messages:
                        last_id = message_id

                        # message_data is already { key: value } as strings
                        # If the JSON is stored in "full_message", parse it:
                        full_msg_str = message_data.get("full_message")
                        level_str = message_data.get("level", 'INFO')
                        if full_msg_str:
                            try:
                                log_entry = json.loads(full_msg_str)
                                # logger.info(f"Parsed JSON log entry: {log_json}")
                                # send_log_to_logdna(log_entry)

                            except json.JSONDecodeError:
                                # logger.warning(f"full_message wasn't valid JSON: {full_msg_str}")
                                log_entry = {"message": full_msg_str}
                        else:
                            log_entry = {"message": str(message_data)}

                        # Or just print the entire dictionary
                        # logger.info("Raw fields from Redis: %s", message_data)
                        level_str = level_str.lower() == "warning" and "warn" or level_str
                        level = getattr(logging, level_str.upper())
                        send_log_to_logdna(log_entry, level=level)

                        await r.xdel(LOG_STREAM, message_id)

            except (RedisConnectionError, TimeoutError) as e:
                logger.error(f"Redis connection error: {e}")
                # Try to reconnect
                r = await get_redis_connection()
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error consuming logs: {e}")
                await asyncio.sleep(0.5)  # brief pause before retrying

    except Exception as e:
        logger.error(f"Fatal error in consume_logs: {e}")
        raise
    finally:
        logger.info('Stopped consuming logs.')
