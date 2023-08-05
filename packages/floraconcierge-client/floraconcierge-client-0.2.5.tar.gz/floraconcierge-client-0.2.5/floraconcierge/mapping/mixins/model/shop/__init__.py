from floraconcierge.client.types import Object


class Currency(Object):
    def __init__(self, *args, **kwargs):
        super(Currency, self).__init__(*args, **kwargs)

        try:
            self.rounding = float(self.rounding)
        except (ValueError, TypeError):
            self.rounding = .0

    def round(self, value, decimals=0):
        if not self.rounding:
            multiplier = float(10 ** decimals)

            return int(value * multiplier) / multiplier
        else:
            return int(self.rounding * int(value / self.rounding))


    def _format(self, value):
        return self.format % value

    def convert(self, value):
        return self._format(self.convert_float(value))

    def convert_float(self, value):
        return self.round(float(self.usdvalue) * float(value), 2)
