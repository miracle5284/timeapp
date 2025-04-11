from fastapi import FastAPI
import asyncio
import logging
from app.consumer import consume_logs
from contextlib import asynccontextmanager

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Logs......")
    # Create and start the task
    task = asyncio.create_task(consume_logs())
    logger.info("Created consume_logs task")
    
    # Wait a bit longer to ensure Redis connection is established
    await asyncio.sleep(2)
    logger.info("Task should be running now")
    
    try:
        yield
    except Exception as e:
        logger.error(f"Error in lifespan: {e}")
        raise
    finally:
        logger.info("Shutting down, cancelling task...")
        # Properly cancel and await the task
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            logger.info("Task cancelled successfully")
        except Exception as e:
            logger.error(f"Error while cancelling task: {e}")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "Logging service is running"}

@app.get("/test-log")
def test_log():
    import logging
    logger = logging.getLogger("chrona.test")
    logger.setLevel("INFO")
    logger.info("This is a test log message from the /test-log endpoint.", extra={"user_id": 999})
    return {"message": "Test log sent!"}

logger.info("Logging service initialized. Listening for logs...")