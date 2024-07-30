"""
This module defines the `YdlLogger` class, which is used to log messages from `yt-dlp`. The logger distinguishes between different log levels and selectively filters out certain messages
"""

import re


class YdlLogger:
    """
    A logger class for handling messages from `yt-dlp`
    """

    def debug(self, msg: str):
        """
        Handles debug messages from `yt-dlp`

        Args:
            msg (str): The message to be logged
        """

        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith("[debug] "):
            # Do nothing
            return
        else:
            self.info(msg)

    def info(self, msg: str):
        """
        Handles info messages from `yt-dlp`

        Args:
            msg (str): The message to be logged
        """

        # Do nothing
        pass

    def warning(self, msg: str):
        """
        Handles warning messages from `yt-dlp`

        Args:
            msg (str): The message to be logged
        """

        # Do nothing for now
        pass

    def error(self, msg: str):
        """
        Handles error messages from `yt-dlp`

        Args:
            msg (str): The message to be logged
        """

        regex_tab_does_not_have_a = re.compile(
            r"\[youtube:tab\] @\w+: This channel does not have a"
        )
        if regex_tab_does_not_have_a.search(msg):
            # Do nothing
            return

        regex_premieres = re.compile(r"\[youtube\] [A-Z0-9]+: Premieres in \d+ ")
        if regex_premieres.search(msg):
            # Do nothing for now
            return

        print(msg)
