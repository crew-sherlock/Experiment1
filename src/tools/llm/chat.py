from promptflow.tools.common import handle_openai_error, \
    to_bool, validate_functions, process_function_call
from src.tools.common import build_messages, post_process_chat_api_response
from src.tools.llm.authentication import BearerAuth
# Avoid circular dependencies: Use import 'from promptflow._internal' instead of 'from
# promptflow' since the code here is in promptflow namespace as well
from promptflow._internal import ToolProvider, tool
from promptflow.contracts.types import PromptTemplate
from openai import AzureOpenAI
from typing import Optional
from promptflow.tracing import trace
from src.tools.common import _try_get_env_var


class AzureOpenAI2(ToolProvider):

    def __init__(self, api_version: str):

        bearer_token = BearerAuth().bearer_token
        self.azure_endpoint = _try_get_env_var("KGW_ENDPOINT")
        self.api_version = api_version
        self._client = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=bearer_token,
            api_version=self.api_version
            )

    # def calculate_cache_string_for_completion(
    #    self,
    #    **kwargs,
    # ) -> str:
    #    d.update({**kwargs})
    #    return json.dumps(d)

    @handle_openai_error()
    def chat(
        self,
        prompt: PromptTemplate,
        # for AOAI, deployment name is customized by user, not model name.
        deployment_name: str,
        temperature: float = 1.0,
        top_p: float = 1.0,
        n: int = 1,
        # stream is a hidden to the end user, it is only supposed to be set by the executor.
        stream: bool = False,
        stop: list = None,
        max_tokens: int = None,
        presence_penalty: float = None,
        frequency_penalty: float = None,
        logit_bias: dict = {},
        user: str = "",
        # function_call can be of type str or dict.
        function_call: object = None,
        functions: list = None,
        # tool_choice can be of type str or dict.
        tool_choice: object = None,
        tools: list = None,
        response_format: object = None,
        seed: int = None,
        **kwargs,
    ):
        messages = build_messages(prompt, **kwargs)
        stream = to_bool(stream)
        params = {
            "model": deployment_name,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stream": stream,
            "extra_headers": {"ms-azure-ai-promptflow-called-from": "aoai-tool"}
        }

        # functions and function_call are deprecated and are replaced by tools and tool_choice.
        # if both are provided, tools and tool_choice are used and functions and function_call are ignored.
        if functions:
            validate_functions(functions)
            params["functions"] = functions
            params["function_call"] = process_function_call(function_call)

        # to avoid vision model validation error for empty param values.
        if stop:
            params["stop"] = stop
        if max_tokens is not None and str(max_tokens).lower() != "inf":
            params["max_tokens"] = int(max_tokens)
        if logit_bias:
            params["logit_bias"] = logit_bias
        if response_format:
            params["response_format"] = response_format
        if seed is not None:
            params["seed"] = seed
        if presence_penalty is not None:
            params["presence_penalty"] = presence_penalty
        if frequency_penalty is not None:
            params["frequency_penalty"] = frequency_penalty
        if user:
            params["user"] = user

        completion = self._client.chat.completions.create(**params)
        return post_process_chat_api_response(completion, stream, functions, tools)


@tool
@trace
def chat(
    prompt: PromptTemplate,
    deployment_name: str,
    api_version: str,
    temperature: float = 1,
    top_p: float = 1,
    n: int = 1,
    stream: bool = False,
    stop: Optional[list] = None,
    max_tokens: Optional[int] = None,
    presence_penalty: Optional[float] = None,
    frequency_penalty: Optional[float] = None,
    logit_bias: Optional[dict] = {},
    user: Optional[str] = "",
    function_call: Optional[object] = None,
    functions: Optional[list] = None,
    tool_choice: Optional[object] = None,
    tools: Optional[list] = None,
    response_format: Optional[object] = None,
    seed: Optional[int] = None,
    **kwargs,
):
    # chat model is not available in azure openai, so need to set the environment
    # variable.
    return AzureOpenAI2(api_version).chat(
        prompt=prompt,
        deployment_name=deployment_name,
        temperature=temperature,
        top_p=top_p,
        n=n,
        stream=stream,
        stop=stop if stop else None,
        max_tokens=max_tokens,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        logit_bias=logit_bias,
        user=user,
        function_call=function_call,
        functions=functions,
        tool_choice=tool_choice,
        tools=tools,
        response_format=response_format,
        seed=seed,
        **kwargs,
    )
