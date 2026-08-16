from apscheduler.schedulers.blocking import BlockingScheduler

from app.services.daily_runner import run_daily_agent


def main():
    scheduler = BlockingScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(
        run_daily_agent,
        "cron",
        hour=8,
        minute=0,
        id="daily-job-agent",
        replace_existing=True,
    )

    print("AI Job Agent scheduler started. Daily run: 08:00 Asia/Kolkata.")
    scheduler.start()


if __name__ == "__main__":
    main()
