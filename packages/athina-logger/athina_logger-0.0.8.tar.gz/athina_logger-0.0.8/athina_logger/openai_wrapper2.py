from dataclasses import dataclass
import datetime
import functools
import inspect
import json
from typing import Callable, Optional
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


class CreateArgsExtractor:
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
            "\n\n Running create args extractor",
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


class OpenAIInjector:
    def __init__(self):
        pass

    def _result_interceptor(
        self, result, athina_meta: dict, send_response: Callable[[dict], None] = None
    ):
        def generator_intercept_packets():
            response = {}
            response["streamed_data"] = []
            for r in result:
                r["athina_meta"] = athina_meta
                response["streamed_data"].append(json.loads(r.__str__()))
                yield r
            send_response(response)

        if inspect.isgenerator(result):
            return generator_intercept_packets()
        else:
            result["athina_meta"] = athina_meta
            send_response(json.loads(result.__str__()))

            return result

    def _result_interceptor_async(
        self, result, athina_meta: dict, send_response: Callable[[dict], None] = None
    ):
        async def generator_intercept_packets():
            response = {}
            response["streamed_data"] = []
            for r in result:
                r["athina_meta"] = athina_meta
                response["streamed_data"].append(json.loads(r.__str__()))
                yield r
            send_response(response)

        if inspect.isgenerator(result):
            return generator_intercept_packets()
        else:
            result["athina_meta"] = athina_meta
            send_response(json.loads(result.__str__()))

            return result

    def _with_athina_auth(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            arg_extractor = CreateArgsExtractor(*args, **kwargs)
            now = datetime.datetime.now()

            print("arg_extractor.get_body()")
            print(arg_extractor.get_args())

            print("arg_extractor.get_athina_meta()")
            print(arg_extractor.get_athina_meta())

            try:
                result = func(**arg_extractor.get_args())
            except Exception as e:
                raise e

            def send_response(response):
                # Log to Athina
                print("send_response response")

            return self._result_interceptor(result, {}, send_response)

        return wrapper

    def _with_athina_auth_async(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # logger = AthinaAsyncLogger.from_athina_global()

            arg_extractor = CreateArgsExtractor(*args, **kwargs)
            now = datetime.datetime.now()

            print("arg_extractor.get_body()")
            print(arg_extractor.get_body())

            print("arg_extractor.get_athina_meta()")
            print(arg_extractor.get_athina_meta())

            def send_response(response):
                print("send_response response")
                print(response)

            return self._result_interceptor_async(result, {}, send_response)

        return wrapper

    def apply_athina_auth(self_parent):
        api_resources_classes = [
            (ChatCompletion, "create", "acreate"),
            (Completion, "create", "acreate"),
            (Edit, "create", "acreate"),
            (Embedding, "create", "acreate"),
            (Image, "create", "acreate"),
            (Moderation, "create", "acreate"),
        ]

        for api_resource_class, method, async_method in api_resources_classes:
            create_method = getattr(api_resource_class, method)
            setattr(
                api_resource_class, method, self_parent._with_athina_auth(create_method)
            )

            async_create_method = getattr(api_resource_class, async_method)
            setattr(
                api_resource_class,
                async_method,
                self_parent._with_athina_auth_async(async_create_method),
            )


print("\n\nInjector Wrapper running\n\n")
injector = OpenAIInjector()
injector.apply_athina_auth()
