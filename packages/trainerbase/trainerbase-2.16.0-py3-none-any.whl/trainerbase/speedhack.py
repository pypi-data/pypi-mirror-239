from pathlib import Path
from typing import override

from pyinjector import inject
from pymem.process import module_from_name

from trainerbase.common import ShortLongSwitch
from trainerbase.gameobject import GameDouble
from trainerbase.memory import ARCH, pm


SPEEDHACK_DLL_MODULE_NAME = f"speedhack{ARCH}.dll"
SPEEDHACK_DLL_PATH = Path(__file__).resolve().parent.parent / "vendor" / SPEEDHACK_DLL_MODULE_NAME
SPEED_MODIFIER_OFFSET = 0x78048 if ARCH == 32 else 0x86040


class SpeedHack:
    def __init__(self):
        self.is_initialized = False
        self._dll_injection_address = self._inject()
        self._speed_modifier = GameDouble(self._dll_injection_address + SPEED_MODIFIER_OFFSET)

        self.factor = 1.0

    def _inject(self) -> int:
        inject(pm.process_id, str(SPEEDHACK_DLL_PATH))  # type: ignore

        speedhack32_address = module_from_name(pm.process_handle, SPEEDHACK_DLL_MODULE_NAME).lpBaseOfDll  # type: ignore

        return speedhack32_address

    @property
    def factor(self):
        return self._speed_modifier.value

    @factor.setter
    def factor(self, value: float):
        self._speed_modifier.value = value

    def disable(self):
        # TODO: Should I eject dll?

        self.factor = 0.0


class SpeedHackShortLongSwitch(ShortLongSwitch):
    @override
    def on_press(self, context: dict):
        speedhack = context["speedhack"]
        dpg_tag = context["dpg_tag"]
        dpg = context["dpg"]
        speedhack.factor = dpg.get_value(dpg_tag)

    @override
    def on_short_press(self, context: dict):
        speedhack = context["speedhack"]

        if context["enabled"]:
            context["enabled"] = False
            speedhack.factor = 1.0
        else:
            context["enabled"] = True
            speedhack.factor = context["dpg"].get_value(context["dpg_tag"])

    @override
    def on_long_press(self, context: dict):
        speedhack = context["speedhack"]
        context["enabled"] = False
        speedhack.factor = 1.0
