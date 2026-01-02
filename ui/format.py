# format.py

def mins_seconds(time):
    """
    Formats a given amount of seconds into a MM:SS string format
    """

    time = int(time)

    # Calculate the amount of full minutes
    minutes = time // 60

    # Find the remaining amount of seconds
    seconds = time % 60

    return f"{minutes:02d}:{seconds:02d}"