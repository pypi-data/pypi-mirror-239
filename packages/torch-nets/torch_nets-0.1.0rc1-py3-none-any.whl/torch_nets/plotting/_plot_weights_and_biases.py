
# -- import packages: ---------------------------------------------------------------
import vinplots
import matplotlib.pyplot as plt


# -- Main operational class:  -------------------------------------------------------
class WeightsBiasesPlot:
    def __init__(self, state_dict, ncols=5, bins=25):
        self.state_dict = state_dict
        self._ncols = ncols
        self._bins = bins

    @property
    def ncols(self):
        if self.nplots > 5:
            self._ncols = self.nplots
        return self._ncols

    @property
    def nplots(self):
        return len(self.state_dict)

    @property
    def cmap(self):
        return {"weight": "#457b9d", "bias": "#a8dadc", "else": "grey"}

    def _mk_plot(self):
        return vinplots.quick_plot(
            nplots=self.nplots,
            ncols=self.ncols,
            wspace=0.2,
            figsize_height=0.5,
            figsize_width=0.5,
        )

    def __call__(self):

        fig, axes = self._mk_plot()
        for n, (key, val) in enumerate(self.state_dict.items()):

            if val.device != "cpu":
                val = val.detach().cpu()
            if "weight" in key:
                color_key = "weight"
            elif "bias" in key:
                color_key = "bias"
            else:
                color_key = "else"

            b = axes[n].hist(
                val.numpy().flatten(), color=self.cmap[color_key], bins=self._bins
            )
            axes[n].set_title(key)


# -- API-facing function: -----------------------------------------------------------
def plot_weights_and_biases(state_dict, ncols=5, bins=25):
    wp = WeightsBiasesPlot(state_dict=state_dict, ncols=ncols, bins=bins)
    return wp()
