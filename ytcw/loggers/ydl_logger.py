import re


class YdlLogger:
    def debug(self, msg: str):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith("[debug] "):
            # Do nothing
            return
        else:
            self.info(msg)

    def info(self, msg: str):
        # Do nothing
        pass

    def warning(self, msg: str):
        # Do nothing for now
        pass

    def error(self, msg: str):
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
