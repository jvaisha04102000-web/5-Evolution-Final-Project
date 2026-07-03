import json
import logging
import os
from datetime import datetime

from config import Config


class EnterpriseLogger:

    def __init__(self):

        os.makedirs("logs", exist_ok=True)

        self.logger = logging.getLogger("AI_PLATFORM")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            # app.log
            app_handler = logging.FileHandler(
                Config.LOG_FILE,
                encoding="utf-8"
            )

            app_handler.setFormatter(formatter)

            # ai_interactions.log
            ai_handler = logging.FileHandler(
               Config.AI_LOG_FILE,
               encoding="utf-8"
            )

            ai_handler.setFormatter(formatter)

            # console
            console_handler = logging.StreamHandler()

            console_handler.setFormatter(formatter)

            self.logger.addHandler(app_handler)
            self.logger.addHandler(ai_handler)
            self.logger.addHandler(console_handler)

        self.activity_file = Config.ACTIVITY_LOG_FILE

        if not os.path.exists(self.activity_file):

            with open(
                self.activity_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )

    def info(
        self,
        message
    ):

        self.logger.info(message)

    def warning(
        self,
        message
    ):

        self.logger.warning(message)

    def error(
        self,
        message
    ):

        self.logger.error(message)

    def log_ai_interaction(

        self,

        module,

        question,

        answer

    ):

        self.logger.info(

            f"[{module}] "

            f"QUESTION: {question}"

        )

        self.logger.info(

            f"[{module}] "

            f"ANSWER: {answer}"

        )

    def log_activity(

        self,

        module,

        action,

        status,

        details=None

    ):

        if details is None:

            details = {}

        record = {

            "timestamp":

                datetime.now().strftime(

                    "%Y-%m-%d %H:%M:%S"

                ),

            "module": module,

            "action": action,

            "status": status,

            "details": details

        }

        with open(

            self.activity_file,

            "r",

            encoding="utf-8"

        ) as file:

            activities = json.load(file)

        activities.append(record)

        with open(

            self.activity_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                activities,

                file,

                indent=4

            )


logger = EnterpriseLogger()