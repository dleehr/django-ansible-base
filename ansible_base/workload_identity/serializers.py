import json

from rest_framework import serializers


class WorkloadIdentitySerializer(serializers.Serializer):
    workload_details = serializers.JSONField()  # This just guarantees the incoming data can be JSON-serialized
    audience = serializers.CharField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # when we POST this we don't want to send nested JSON, we want to send a JSON string
        ret['workload_details'] = json.dumps(ret['workload_details'], sort_keys=True)
        return ret
