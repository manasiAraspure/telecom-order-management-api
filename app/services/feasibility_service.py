import logging
import time
import random

logger = logging.getLogger(__name__)


def check_feasibility(latitude: str, longitude: str) -> dict:
    """
    Simulates calling an external feasibility-check API
    (e.g. a fiber network coverage service) using subscriber coordinates.

    In a real system, this would be an HTTP call like:
        response = requests.get(EXTERNAL_API_URL, params={...}, timeout=5)

    Here we simulate that behavior, including a small delay
    (like a real network call would have)
    """
    logger.info(f"Checking feasibility for lat={latitude}, lon={longitude}")

    try:
        lat = float(latitude.replace("°", "").replace("N", "").replace("S", "").strip())
        lon = float(longitude.replace("°", "").replace("E", "").replace("W", "").strip())
    except ValueError:
        logger.warning("Invalid coordinates received")
        return {"feasible": False, "reason": "Invalid coordinates"}

    # Simulate network latency, like a real external API call
    time.sleep(0.5)

    # Simple mock rule: within Hyderabad's rough coordinate range = feasible
    is_within_service_area = (17.2 <= lat <= 17.6) and (78.2 <= lon <= 78.6)

    if is_within_service_area:
        logger.info("Feasibility check passed")
        return {"feasible": True, "reason": "Location within fiber service area"}
    else:
        logger.info("Feasibility check failed")
        return {"feasible": False, "reason": "Location outside current fiber service area"}