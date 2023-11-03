from ...interface import IPacker


class BarGraphParamDataPacker(IPacker):
    def __init__(self, obj) -> None:
        super().__init__(obj)

    def obj_to_tuple(self):
        return [str(self._obj.ID), str(self._obj.Name), int(self._obj.Style), int(self._obj.FrameStyle),
                str(self._obj.Color), int(self._obj.LineWidth), int(self._obj.PlotIndex), int(self._obj.ValueAxisID),
                bool(self._obj.ShowLegend), str(self._obj.LegendFormat), str(self._obj.LegendColor), bool(self._obj.JoinValueAxis),
                float(self._obj.TickValidMul), float(self._obj.ValidMaxValue), float(self._obj.ValidMinValue), dict(self._obj.UserData)]

    def tuple_to_obj(self, t):
        if len(t) >= 16:
            self._obj.ID = t[0]
            self._obj.Name = t[1]
            self._obj.Style = t[2]
            self._obj.FrameStyle = t[3]
            self._obj.Color = t[4]
            self._obj.LineWidth = t[5]
            self._obj.PlotIndex = t[6]
            self._obj.ValueAxisID = t[7]
            self._obj.ShowLegend = t[8]
            self._obj.LegendFormat = t[9]
            self._obj.LegendColor = t[10]
            self._obj.JoinValueAxis = t[11]
            self._obj.TickValidMul = t[12]
            self._obj.ValidMaxValue = t[13]
            self._obj.ValidMinValue = t[14]
            self._obj.UserData = t[15]

            return True
        return False
