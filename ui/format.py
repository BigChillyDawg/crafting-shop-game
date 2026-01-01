# format.py

def mins_seconds(time):
    """
    Formats a given amount of seconds into a MM:SS string format
    """

    # Calculate the amount of full minutes
    minutes = time // 60

    # Find the remaining amount of seconds
    seconds = time % 60

    return f"{minutes:2d}:{seconds:2d}"