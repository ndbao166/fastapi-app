import sys

from loguru import logger


class Logger:
    @staticmethod
    def setup(
        folder_path: str,
        folder_backup_path: str,
    ) -> None:
        logger.remove()
        Logger._add_console_handler()
        Logger._add_file_handler(folder_path, folder_backup_path)
        logger.info("🚀 Logger has been setup.")

    @staticmethod
    def _add_console_handler() -> None:
        logger.add(sys.stdout, level="DEBUG", colorize=True)

    @staticmethod
    def _add_file_handler(folder_path: str, folder_backup_path: str) -> None:
        # 1. MAIN LOG FILE - Luôn có
        logger.add(
            f"{folder_path}/app.log",
            level="INFO",
            rotation="10 MB",  # Rotate khi 10MB
            retention="30 days",  # Giữ 30 ngày
            compression="zip",  # Nén file cũ
            enqueue=True,  # Async, không block app
            encoding="utf-8",  # Support tiếng Việt
        )

        # 2. ERROR LOG - Chỉ lỗi
        logger.add(
            f"{folder_path}/error.log",
            level="ERROR",
            rotation="50 MB",  # File lớn hơn vì ít lỗi
            retention="90 days",  # Giữ lâu hơn để investigate
            compression="zip",
            backtrace=True,  # Full stack trace
            diagnose=True,  # Debug info
            enqueue=True,
        )

        # 3. DEBUG LOG - Chỉ trong development
        logger.add(
            f"{folder_path}/debug.log",
            level="DEBUG",
            rotation="100 MB",
            retention="7 days",  # Debug không cần giữ lâu
            enqueue=True,
        )

        # 4. backup log
        logger.add(
            f"{folder_backup_path}/backup_{{time}}.log",
            level="DEBUG",
            rotation="1 minute",
        )
