"""
Scheduler base configuration for running periodic ETL jobs.
Uses APScheduler with ThreadPoolExecutor for parallel job execution.
"""

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import logging

from finhub_etl.scheduler.jobs.us_exchange_jobs import (
    us_premarket_open_job,
    us_postmarket_close_job,
)
from finhub_etl.scheduler.jobs.uae_exchange_jobs import (
    uae_market_open_job,
    uae_market_close_job,
)
from finhub_etl.scheduler.jobs.uk_exchange_jobs import (
    uk_market_open_job,
    uk_market_close_job,
)

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

    # US Exchange Jobs
    scheduler.add_job(
        func=us_premarket_open_job,
        trigger=CronTrigger(hour=12, minute=0),
        id="us_premarket_open",
        name="US Pre-Market Open (12:00 IST)",
        replace_existing=True,
    )

    scheduler.add_job(
        func=us_postmarket_close_job,
        trigger=CronTrigger(hour=4, minute=0),
        id="us_postmarket_close",
        name="US Post-Market Close (04:00 IST)",
        replace_existing=True,
    )

    # UAE Exchange Jobs
    scheduler.add_job(
        func=uae_market_open_job,
        trigger=CronTrigger(hour=10, minute=0),
        id="uae_market_open",
        name="UAE Market Open (10:00 IST)",
        replace_existing=True,
    )

    scheduler.add_job(
        func=uae_market_close_job,
        trigger=CronTrigger(hour=14, minute=45),
        id="uae_market_close",
        name="UAE Market Close (14:45 IST)",
        replace_existing=True,
    )

    # UK Exchange Jobs
    scheduler.add_job(
        func=uk_market_open_job,
        trigger=CronTrigger(hour=11, minute=0),
        id="uk_market_open",
        name="UK Market Open (11:00 IST)",
        replace_existing=True,
    )

    scheduler.add_job(
        func=uk_market_close_job,
        trigger=CronTrigger(hour=20, minute=30),
        id="uk_market_close",
        name="UK Market Close (20:30 IST)",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("✅ Scheduler started successfully with 6 exchange jobs")

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
