from .base_provider import BaseProvider
import json
import tornadoredis.pubsub
import tornadoredis


class RedisSubProvider(BaseProvider):
    def __init__(self):
        self._subscriber = tornadoredis.pubsub.SockJSSubscriber(tornadoredis.Client())

    def close(self, broadcaster):
        for channel in self._subscriber.subscribers:
            if broadcaster in self._subscriber.subscribers[channel]:
                self._subscriber.unsubscribe(channel, broadcaster)

    def get_channel(self, base_channel, **channel_filter):
        return self._construct_channel(base_channel, **channel_filter)

    def subscribe(self, channels, broadcaster):
        self._subscriber.subscribe(channels, broadcaster)

    def unsubscribe(self, channels, broadcaster):
        for channel in channels:
            if broadcaster in self._subscriber.subscribers[channel]:
                self._subscriber.subscribers[channel].pop(broadcaster)

    def publish(self, channel, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        broadcasters = list(self._subscriber.subscribers[channel].keys())
        if broadcasters:
            for bc in broadcasters:
                if not bc.session.is_closed:
                    bc.broadcast(broadcasters, data)
                    break
