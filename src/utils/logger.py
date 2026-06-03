import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from rich.logging import RichHandler
from rich.traceback import install

# 全局安装 rich 异常美化，只执行一次
install(show_locals=True)

_initialized = False


def get_logger(name: str) -> logging.Logger:
    """获取 logger 实例，handler 只在首次调用时配置。"""
    global _initialized
    logger = logging.getLogger(name)

    if not _initialized:
        _setup_root_handlers()
        _initialized = True

    return logger


def _setup_root_handlers():
    """配置根 logger 的 handler（控制台 + 文件轮转）。"""
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    if root.hasHandlers():
        return  # 已配置，跳过

    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # 控制台 handler
    console_handler = RichHandler(
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        level=logging.INFO,
    )
    console_format = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    console_handler.setFormatter(console_format)

    # 文件 handler（按天轮转）
    file_handler = TimedRotatingFileHandler(
        filename=log_dir / "app.log",
        when="midnight",
        backupCount=7,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s"
    )
    file_handler.setFormatter(file_format)

    root.addHandler(console_handler)
    root.addHandler(file_handler)
