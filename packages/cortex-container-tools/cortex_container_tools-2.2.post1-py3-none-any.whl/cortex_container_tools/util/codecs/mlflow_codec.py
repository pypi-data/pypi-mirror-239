import pandas as pd
import numpy as np

from mlserver.types.dataplane import InferenceRequest, RequestInput
from mlserver.codecs import PandasCodec, NumpyCodec, StringCodec
from typing import Any, List, Optional, Union

from ._codec import Codec
import json

class MLflowCodec(Codec):
    def decode(data):
        request = InferenceRequest(**json.loads(data))
        content_type = request.parameters.content_type
        if content_type == 'pd':
            return PandasCodec.decode_request(request)
        elif content_type == 'np':
            return NumpyCodec.decode(request)
        elif content_type == 'str':
            return StringCodec.decode(RequestInput(**request.inputs[0]))
        else:
            raise ValueError(f"Unsupported content type: {content_type}")

    def encode(data):
        input_type = type(data)
        if input_type == pd.DataFrame:
            return PandasCodec.encode_outputs(data)
        elif input_type == np.ndarray:
            return NumpyCodec.encode_output('output-0', data)
        elif input_type == str:
            return StringCodec.encode(data)
        else:
            raise ValueError(f"Unsupported content type: {InferenceRequest.parameters.content_type}")
