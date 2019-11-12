
class BreakItem:
    start = None
    end = None


class ClockRowItem:

    clock_in = None
    breaks = set()
    clock_out = None

    def __eq__(self, other):
        if not isinstance(other, ClockRowItem):
            return False
        return self.clock_in == other.clock_in and self.clock_out == other.clock_out and self.breaks == other.breaks
