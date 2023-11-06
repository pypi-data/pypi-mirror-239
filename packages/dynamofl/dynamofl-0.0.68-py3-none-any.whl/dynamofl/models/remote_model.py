from ..Request import _Request

from ..models.model import Model
from typing_extensions import Optional


class RemoteModel(Model):
    def __init__(
        self,
        request,
        name: str,
        key: str,
        id: str,
        config,
    ) -> None:
        self.request = request
        super().__init__(
            request=request,
            name=name,
            key=key,
            config=config,
            type="REMOTE",
            id=id,
        )

    @staticmethod
    def create_and_upload(
        request: _Request,
        name: str,
        key: str,
        api_provider: str,
        api_instance: str,
        endpoint: Optional[str],
    ):
        config = {
            "remoteModelApiProvider": api_provider,
            "remoteModelApiInstance": api_instance,
            "remoteModelEndpoint": endpoint,
        }

        model_id = Model.create_ml_model_and_get_id(
            request=request, name=name, key=key, type="REMOTE", config=config, size=None
        )

        return RemoteModel(
            request=request,
            name=name,
            key=key,
            config=config,
            id=model_id,
        )
