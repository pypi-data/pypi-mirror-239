from dataclasses import dataclass
import datetime
import functools
import inspect
import json
import tiktoken
import tiktoken_ext.openai_public
from typing import Callable, Optional, List
import openai  # noqa
from openai.api_resources import (
    ChatCompletion,
    Completion,
    Edit,
    Embedding,
    Image,
    Moderation,
)


@dataclass
class AthinaMeta:
    customer_id: Optional[str] = None
    customer_user_id: Optional[str] = None


class OpenAiArgsExtractor:
    _athina_meta: Optional[AthinaMeta]

    def __init__(
        self,
        api_key=None,
        api_base=None,
        api_type=None,
        request_id=None,
        api_version=None,
        organization=None,
        **kwargs
    ):
        print(
            "\n\n Running args extractor",
            kwargs,
        )
        self.kwargs = kwargs
        self.kwargs["api_key"] = api_key
        self.kwargs["api_base"] = api_base
        self.kwargs["api_type"] = api_type
        self.kwargs["request_id"] = request_id
        self.kwargs["api_version"] = api_version
        self.kwargs["organization"] = organization
        self._athina_meta = kwargs.get("athina_meta")
        self.kwargs.pop("athina_meta", None)

    def get_args(self):
        return self.kwargs

    def get_athina_meta(self):
        return self._athina_meta


def num_tokens_from_string(string: str, model: str) -> int:
    """Returns the number of tokens in a text string."""
    # encoding_name = tiktoken.encoding_for_model(model)
    # encoding = tiktoken.get_encoding(encoding_name)
    # num_tokens = len(encoding.encode(string))
    return round(len(string) / 4)


def handle_streamed_chunks(openai_response):
    for r in openai_response:
        yield json.loads(r.__str__())


def build_response_from_stream(prompt, openai_response):
    print("\n\nbuild_response_from_stream running\n\n")
    # Create an empty array to store the streamed data
    streamed_data_array = []

    response_data = {}
    # Call the handle_streamed_data function and iterate over the generator
    for chunk in handle_streamed_chunks(openai_response):
        response_data = {**chunk}
        print("chunk", chunk)
        if ("choices" in chunk) and (len(chunk["choices"]) > 0):
            chunk_choice = chunk["choices"][0]
            if "delta" in chunk_choice and "content" in chunk_choice["delta"]:
                content = chunk_choice["delta"]["content"]
                streamed_data_array.append(content)

    # Now you can access the streamed data in the array
    print(streamed_data_array)
    response_str = "".join(streamed_data_array)
    open_ai_response_obj = construct_open_ai_response_from_stream(
        prompt, response_data, response_str
    )
    return open_ai_response_obj


# This method constructs a response object with the same format as the non-streamed response object
def construct_open_ai_response_from_stream(
    prompt: str, chunk_obj: dict, response_str: str
):
    response_data = {**chunk_obj}
    response_data["object"] = "chat.completion"
    response_data["choices"][0]["delta"] = None
    response_data["choices"][0]["index"] = 0
    response_data["choices"][0]["finish_reason"] = "stop"
    response_data["choices"][0]["message"] = {
        "role": "assistant",
        "content": response_str,
    }
    response_data["choices"][0] = {
        k: v for k, v in response_data["choices"][0].items() if v is not None
    }
    model = response_data["model"]

    # Get token usage counts
    prompt_tokens = num_tokens_from_string(prompt, model)
    completion_tokens = num_tokens_from_string(response_str, model)
    total_tokens = prompt_tokens + completion_tokens
    response_data["usage"] = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }
    return response_data


class OpenAiMiddleware:
    def __init__(self):
        pass

    def _build_result_object(
        self,
        prompt_messages: List[dict],
        openai_response: dict,
        athina_meta: dict,
    ) -> dict:
        result = {}
        if inspect.isgenerator(openai_response):
            print("\n\nopenai_response is a stream")
            result["athina_meta"] = athina_meta
            prompt = " ".join(list(map(lambda p: p["content"], prompt_messages)))
            result = build_response_from_stream(prompt, openai_response)
        else:
            print("\n\nopenai_response is NOT a stream")
            result["athina_meta"] = athina_meta
            result = json.loads(openai_response.__str__())

        return result

    def _with_athina_logging(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract args from OpenAI call
            arg_extractor = OpenAiArgsExtractor(*args, **kwargs)
            print("\n\narg_extractor.get_args()", arg_extractor.get_args())

            # Generate the result
            openai_response = func(**arg_extractor.get_args())
            print("\n\openai_response", openai_response)

            if openai_response is None:
                raise Exception("No result was returned from OpenAI")

            prompt_messages = arg_extractor.get_args()["messages"]
            athina_meta = arg_extractor.get_athina_meta()

            result = self._build_result_object(
                prompt_messages=prompt_messages,
                openai_response=openai_response,
                athina_meta=athina_meta,
            )

            # Log to Athina
            # log_to_athina(result, arg_extractor.get_args())
            return result

        return wrapper

    def apply_athina(self_parent):
        api_resources_classes = [
            (ChatCompletion, "create", "acreate"),
            # (Completion, "create", "acreate"),
        ]

        for api_resource_class, method, async_method in api_resources_classes:
            create_method = getattr(api_resource_class, method)
            setattr(
                api_resource_class,
                method,
                self_parent._with_athina_logging(create_method),
            )


print("\n\nInjector Wrapper running\n\n")
middleware = OpenAiMiddleware()
middleware.apply_athina()
