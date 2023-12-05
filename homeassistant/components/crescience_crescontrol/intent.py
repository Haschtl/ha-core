"""Crescontrol intents."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.intent import Intent, IntentResponse

from .const import DOMAIN
from .crescience.crescontrol import CresControl
from .crescontrol_devices import STATIC_CRESCONTROL_FEATURES, IntentDefinition

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create static BinarySensor entities for entry."""
    uid = config_entry.data.get("uid")
    device = hass.data[DOMAIN]["devices"].get(uid)

    for intent_type, config in STATIC_CRESCONTROL_FEATURES["intents"].items():
        intent.async_register(
            hass, CresControlIntent(hass, device, intent_type, config)
        )


class CresControlIntent(intent.IntentHandler):
    """CresControl Intent Entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        device: CresControl,
        intent_type: str,
        config: IntentDefinition,
    ) -> None:
        """Create new CresControl Button Entity."""
        self._device = device
        self._config = config
        self.intent_type = intent_type

    def async_can_handle(self, intent_obj: Intent) -> bool:
        """Check if the intent can be handled."""
        return False

    async def async_handle(self, intent_obj: Intent) -> IntentResponse:
        """Handle the intent."""
        return await super().async_handle(intent_obj)
