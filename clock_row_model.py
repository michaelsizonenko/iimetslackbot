from datetime import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M"


class BreakItem:
    start = None
    end = None


class ClockRowItem:

    __clock_in = None
    __breaks = set()
    __clock_out = None

    def __init__(self, clock_in=None, breaks=(), clock_out=None):
        self.__clock_in = clock_in
        self.__breaks = set(breaks)
        self.__clock_out = clock_out

    def __eq__(self, other):
        if not isinstance(other, ClockRowItem):
            return False
        return self.__clock_in == other.__clock_in and self.__clock_out == other.__clock_out and self.__breaks == other.__breaks

    def set_clock_in(self):
        self.__clock_in = datetime.utcnow()

    def get_clock_in(self):
        return self.__clock_in

    def set_clock_out(self):
        self.__clock_out = datetime.utcnow()

    def get_clock_out(self):
        return self.__clock_out

    def to_google_list(self):
        str_clock_in = self.__clock_in.strftime(DATE_FORMAT) if self.__clock_in else ""
        str_breaks = ""
        str_clock_out = self.__clock_out.strftime(DATE_FORMAT) if self.__clock_out else ""
        return [str_clock_in, str_breaks, str_clock_out]
