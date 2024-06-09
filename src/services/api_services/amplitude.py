from concurrent.futures import ThreadPoolExecutor
from amplitude import Amplitude, BaseEvent
from config import settings

amplitude = Amplitude(settings.amplitude_api_key)


executor_pool = ThreadPoolExecutor(max_workers=1)


def send_event(event_name: str, user_id: str, event_properties: dict):
    event = BaseEvent(
        user_id=user_id,
        event_type=event_name,
        event_properties=event_properties
    )
    amplitude.track(
        event=event
    )

def log_event(event_name: str, user_id: str, event_properties: dict):
    executor_pool.submit(send_event, event_name, user_id, event_properties)
