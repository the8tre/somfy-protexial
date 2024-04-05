from .const import Zone, Zones


def zones_to_zone_array(zones) -> list[Zone]:
    match zones:
        case Zones.AB:
            return [Zone.A, Zone.B]
        case Zones.BC:
            return [Zone.B, Zone.C]
        case Zones.AC:
            return [Zone.A, Zone.C]
        case Zones.A:
            return [Zone.A]
        case Zones.B:
            return [Zone.B]
        case Zones.C:
            return [Zone.C]


def ints_to_zone_array(int_zones: list[int]) -> list[Zone]:
    if int_zones is None:
        return None
    return list(map(lambda z: Zone(z), int_zones))


def zones_from_zone_array(zones: list[Zone]):
    if zones is None:
        return Zones.NONE
    if len(zones) == 1:
        match zones[0]:
            case Zone.A:
                return Zones.A
            case Zone.B:
                return Zones.B
            case Zone.B:
                return Zones.C
    elif set(zones).issubset([Zone.A, Zone.B]):
        return Zones.AB
    elif set(zones).issubset([Zone.A, Zone.C]):
        return Zones.AC
    elif set(zones).issubset([Zone.B, Zone.C]):
        return Zones.BC
