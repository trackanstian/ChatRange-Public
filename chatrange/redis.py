import os
import redis
import fakeredis


from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

REDIS_EMULATOR = os.getenv('REDIS_EMULATOR', False)
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', '13997')
REDIS_DB = os.getenv('REDIS_DB', '0')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')


def get_redis_client():
    if REDIS_EMULATOR == False:
        # Use fakeredis for testing
        return fakeredis.FakeStrictRedis()
    else:
        # Use real Redis in production
        #return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password="M3y0qXRNu6WEWvJfhdTZIR3ysahYZdaP")
        return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)