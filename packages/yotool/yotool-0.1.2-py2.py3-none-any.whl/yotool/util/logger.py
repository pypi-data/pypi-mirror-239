def log(*args) -> None:
    print(*args)

class Logger:
    head_color = 94
    info_info = f'\033[{head_color}m[yotool]\033[0m'
    warning_info = "[yotool] Warning:"
    error_info = "[yotool] Error:"

    def __init__(self):
        pass

    @classmethod
    def log(cls, msg: str) -> None:
        assert len(msg) > 0
        log(msg)

    @classmethod
    def info(cls, msg: str) -> None:
        assert len(msg) > 0
        log(cls.info_info, msg)

    @classmethod
    def warning(cls, msg: str) -> None:
        assert len(msg) > 0
        log(cls.info_info, msg)

    @classmethod
    def error(cls, msg: str) -> None:
        assert len(msg) > 0
        log(cls.info_info, msg)


if __name__ == "__main__":
    Logger.info("hello word")
