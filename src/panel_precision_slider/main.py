import panel as pn
import param
import panel as pn


class PrecisionSlider(pn.custom.PyComponent):

    value = param.Number(default=5)
    min = param.Number(default=0, readonly=True)
    max = param.Number(default=10, readonly=True)
    step = param.Number(default=0.1)
    show_step = param.Boolean(default=False, label="")
    swap = param.Boolean(default=False, label="")

    def __init__(self, **params):
        super().__init__(**params)

        self._swap_icon = pn.widgets.ToggleIcon.from_param(
            self.param.swap,
            icon="refresh",
            active_icon="adjustments-horizontal",
            margin=0,
        )
        self._show_icon = pn.widgets.ToggleIcon.from_param(
            self.param.show_step, icon="eye", active_icon="eye-off", margin=0
        )
        self._placeholder = pn.pane.Placeholder()
        self._value_input = pn.widgets.FloatInput(
            value=self.param.value,
            start=self.param.min,
            end=self.param.max,
            step=self.param.step,
        )
        self._value_slider = pn.widgets.FloatSlider.from_param(
            self._value_input.param.value,
            start=self.param.min,
            end=self.param.max,
            step=self.param.step,
        )
        self._step_slider = pn.widgets.FloatSlider.from_param(
            self.param.step, start=0.001, step=0.001, visible=self.param.show_step
        )
        self.param.trigger("swap")

    @param.depends("swap", watch=True)
    def _swap_widgets(self):
        if self.swap:
            self._placeholder.update(self._value_input)
        else:
            self._placeholder.update(pn.Column(self._value_slider, self._step_slider))

    def __panel__(self):
        return pn.Column(
            self._placeholder,
            pn.Row(self._swap_icon, self._show_icon, margin=(1, 10)),
        )
