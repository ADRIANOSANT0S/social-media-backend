from rest_framework.serializers import CharField, ModelSerializer

from apps.auths.services.email_change_services import EmailChangeServices
from apps.core.utils import run_validation
from apps.users.models import User


class RequestRecoverEmailCodeSerializer(ModelSerializer):
    """
    Serializer for request the recover email code.
    """

    recover_email_code = CharField(required=True, max_length=12)

    class Meta:
        model = User
        fields = ["recover_email_code"]

    def validate_recover_email_code(self, value):
        service = EmailChangeServices(user=self.instance)
        return run_validation(service.verify_code, value)
