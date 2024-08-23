from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken as BaseAccessToken

User = get_user_model()


class AccessToken(BaseAccessToken):
    def get_user(self):
        if "user_id" in self.payload:
            return User.objects.get(self.payload["user_id"])

    @property
    def user(self):
        return self.get_user()

    @property
    def auth_header(self):
        return {"Authorization": "Bearer {}".format(self)}
