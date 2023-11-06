from typing import Optional
from ..Request import _Request
from ..file_transfer.upload import FileUploader, ParamsArgs

from ..models.model import Model

CHUNK_SIZE = 1024 * 1024  # 1MB


class LocalModel(Model):
    def __init__(
        self, request, name: str, key: str, id: str, config, size: int
    ) -> None:
        self.request = request
        self.size = size
        super().__init__(
            request=request,
            name=name,
            key=key,
            config=config,
            type="LOCAL",
            id=id,
        )

    @staticmethod
    def create_and_upload(
        request: _Request,
        name: str,
        key: Optional[str],
        model_file_path: str,
        config,
        peft_config_path: Optional[str] = None,
    ):
        upload_response = LocalModel.upload_model(
            request=request, key=key, model_file_path=model_file_path
        )
        new_key = upload_response["modelEntityKey"]
        config["objKey"] = upload_response["modelObjectKey"]
        file_size = upload_response["fileSize"]

        if peft_config_path:
            config["peftConfigS3Key"] = LocalModel.upload_peft_file(
                request=request, peft_config_path=peft_config_path
            )

        model_id = Model.create_ml_model_and_get_id(
            request=request,
            name=name,
            key=new_key,
            type="LOCAL",
            config=config,
            size=file_size,
        )

        return LocalModel(
            request=request,
            name=name,
            key=new_key,
            config=config,
            id=model_id,
            size=file_size,
        )

    @staticmethod
    def upload_model(request: _Request, key: Optional[str], model_file_path: str):
        response = LocalModel.upload_model_file(
            request=request, key=key, model_file_path=model_file_path
        )
        return {
            "modelObjectKey": response.presigned_endpoint_response["objKey"],
            "modelEntityKey": response.presigned_endpoint_response["entityKey"],
            "fileSize": response.file_size,
        }

    @staticmethod
    def upload_peft_file(request: _Request, peft_config_path):
        response = LocalModel.upload_model_file(
            request=request, key=None, model_file_path=peft_config_path
        )
        return response.presigned_endpoint_response["objKey"]

    @staticmethod
    def upload_model_file(request: _Request, key: Optional[str], model_file_path: str):
        def construct_params(params_args: ParamsArgs):
            params = {
                "filename": params_args.file_name,
                "sha1Checksum": params_args.sha1hash,
            }
            if key:
                params["key"] = key
            return params

        file_uploader = FileUploader(request)
        response = file_uploader.upload_file(
            file_path=model_file_path,
            presigned_endpoint_url="/ml-model/presigned-url",
            construct_params=construct_params,
        )
        return response
