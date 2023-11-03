"""cnmpdk straight waveguide."""
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.cross_section import CrossSectionSpec
import warnings

from cnmpdk.tech import deep, shallow, heater, trench

@gf.cell
def cnm_straight(
    length: float = 10.0,
    npoints: int = 2,
    width: float | None = None,
    cross_section: CrossSectionSpec = "cnm_deep",
    layer: gf.typings.LayerSpec | None = None,
) -> Component:
    """Returns a Straight waveguide.

    Args:
        length: straight length (um).
        npoints: number of points.
        layer: layer to use. Defaults to cross_section.layer.
        width: width to use. Defaults to cross_section.width.
        add_pins: add pins to the component.
        cross_section: specification (CrossSection, string or dict).

    .. code::

        o1 -------------- o2
                length
    """

    if width < 0.6:
        raise ValueError(f"The litho resolution is 0.6")
    else:
        match cross_section: 
            case "cnm_deep":
                cross_section = gf.partial(deep, width=width)
            case "cnm_shallow":
                cross_section = gf.partial(shallow, width=width)
            case "cnm_heater":
                cross_section = gf.partial(heater, width=width)
            case "cnm_trench":
                cross_section = gf.partial(trench, width=width)
    
    c = Component()
    c.add_ref(gf.components.straight(length=length, width=width, npoints=npoints, cross_section=cross_section))

    return c

if __name__ == "__main__":
    import gdsfactory as gf

    c = cnm_straight(cross_section="cnm_deep")
    # c = straight()
    print(c.info)
    c.show(show_ports=True)