




def create_scheduler():
    executors = {
        "default": ThreadPoolExecutor(max_workers=32)  # allow 20 parallel jobs
    }
    scheduler = BackgroundScheduler(executors=executors)

    # // Remove the data older than two days
    scheduler.add_job(
        func=truncate_data_older_than_2days,
        trigger=CronTrigger(
            hour=4,
            minute=0,
        ),
        id="truncate_old_stock_data",
        name="Truncate BSE stock data older than 2 days (Runs daily at 4:00 AM)",
        replace_existing=True,
    )

    

    scheduler.start()
    print("✅ Scheduler started.")

    return scheduler