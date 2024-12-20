from __future__ import annotations

from lib.common import grid_input


class Region:
    __slots__ = 'plots'

    plots: set[Plot]

    def __init__(self, plots: set[Plot]):
        self.plots = plots

    def merge(self, region: Region):
        self.plots.update(region.plots)
        for added_plot in region.plots:
            added_plot.region = self

    def fence_price(self):
        return len(self.plots) * sum(plot.perimeter for plot in self.plots)


class Plot:
    __slots__ = 'plant', 'region', 'perimeter'

    plant: str
    region: Region
    perimeter: int

    def __init__(self, plant: str):
        self.plant = plant
        self.region = Region({self})
        self.perimeter = 4

    def add_compatible(self, plot: Plot, regions: set[Region]) -> bool:
        if self.plant == plot.plant:
            self.perimeter -= 1
            plot.perimeter -= 1
            if self.region != plot.region:
                regions.remove(plot.region)
                self.region.merge(plot.region)
            return True
        return False


@grid_input(str)
def get_fence_price(rows: list[list[str]]) -> int:
    return sum(region.fence_price() for region in _read_regions(rows))


def _read_regions(rows: list[list[str]]) -> set[Region]:
    regions = set()
    up_plots = None
    for i, row in enumerate(rows):
        left_plot = None
        current_plots = []
        for j, cell in enumerate(row):
            plot = Plot(cell)
            regions.add(plot.region)
            if up_plots is not None:
                up_plots[j].add_compatible(plot, regions)
            if left_plot is not None:
                left_plot.add_compatible(plot, regions)
            current_plots.append(plot)
            left_plot = plot
        up_plots = current_plots
    return regions
