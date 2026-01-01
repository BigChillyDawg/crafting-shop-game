# cooldown.py

import time

class Cooldown:
    """
    Tracks time-based cooldowns for actions.

    A cooldown becomes ready once `duration` seconds have passed
    since the last time it was triggered.
    """
    def __init__(self, duration, last_used=0):
        self.duration = duration
        self.last_used = last_used

    def is_ready(self):
        """ Returns True if the cooldown is ready to be triggered. """

        current_time = time.time()
        return (self.last_used + self.duration) <= current_time
    
    def trigger(self):
        """ Triggers the cooldown if it is ready. """
        if self.is_ready():
            self.last_used = time.time()
            return True
        else:
            return False
        
    def remaining(self):
        """ Returns the remaining time on the cooldown in seconds. """

        remaining = (self.last_used + self.duration) - time.time()
        if remaining <= 0:
            return 0
        return remaining
    
    def reset(self):
        """ Resets the cooldown to be ready immediately. """

        self.last_used = 0
        