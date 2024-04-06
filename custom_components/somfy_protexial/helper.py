from .const import Zone


def int_to_zones(int_zones: int) -> list[Zone]:
    match int_zones:
        case 0:
            return [Zone.NONE]
        case 1:
            return [Zone.A]
        case 2:
            return [Zone.B]
        case 4:
            return [Zone.C]
        case 3:
            return [Zone.A, Zone.B]
        case 6:
            return [Zone.B, Zone.C]
        case 5:
            return [Zone.A, Zone.C]
