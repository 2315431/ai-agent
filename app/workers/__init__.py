from redis import Redis
from rq import Queue
import os

# Redis connection
redis_conn = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

# Task queues
task_queue = Queue("content_tasks", connection=redis_conn)
embedding_queue = Queue("embedding_tasks", connection=redis_conn)
generation_queue = Queue("generation_tasks", connection=redis_conn)

__all__ = ["task_queue", "embedding_queue", "generation_queue"]
