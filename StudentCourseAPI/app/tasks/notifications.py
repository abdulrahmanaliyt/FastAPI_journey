import logging

logger = logging.getLogger("student_course_api")


def send_welcome_notification(email: str):
    logger.info(
        "Welcome notification started for %s",
        email
    )

    # Email delivery will be integrated later.
    logger.info(
        "Welcome notification completed for %s",
        email
    )