"""
Scheduler base configuration for running periodic ETL jobs.
Uses APScheduler with ThreadPoolExecutor for parallel job execution.
"""

from concurrent.futures import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import logging

logger = logging.getLogger(__name__)


def create_scheduler():
    """
    Create and configure the background scheduler with thread pool executor.

    Returns:
        BackgroundScheduler: Configured scheduler instance
    """
    executors = {
        "default": ThreadPoolExecutor(max_workers=32)  # Allow 32 parallel jobs
    }

    scheduler = BackgroundScheduler(executors=executors)

    # Example job configuration:
    # scheduler.add_job(
    #     func=your_job_function,
    #     trigger=CronTrigger(
    #         hour=0,
    #         minute=0,
    #     ),
    #     id="unique_job_id",
    #     name="Job description",
    #     replace_existing=True,
    # )

    # Example interval job:
    # scheduler.add_job(
    #     func=your_interval_function,
    #     trigger=IntervalTrigger(hours=1),
    #     id="interval_job_id",
    #     name="Runs every hour",
    #     replace_existing=True,
    # )

    scheduler.start()
    logger.info("✅ Scheduler started successfully")

    return scheduler


def shutdown_scheduler(scheduler):
    """
    Gracefully shutdown the scheduler.

    Args:
        scheduler: BackgroundScheduler instance to shutdown
    """
    if scheduler:
        scheduler.shutdown(wait=True)
        logger.info("🛑 Scheduler shutdown complete")
