from datetime import timedelta
import logging
from numpy import floor

logger = logging.getLogger("uvicorn")


def pace_to_string(pace: float) -> str:
    """Create a pace string in the format
    X:XX min/km

    :param pace: pace in mins per km
    :return: human formatted pace
    """
    logger.info(pace)
    pace_bits = str(timedelta(seconds=60 * pace)).split(":")  # H:M:S
    logger.info(pace_bits)
    mins = pace_bits[1]
    if mins[0] == "0":
        mins = mins[1:]
    seconds = pace_bits[2][:2]
    pace_str = f"{mins}:{seconds} mins/km"
    return pace_str
