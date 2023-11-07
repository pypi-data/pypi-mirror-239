import logging

from satosa.base import STATE_KEY as STATE_KEY_BASE
from satosa.context import Context
from satosa.internal import InternalData
from satosa.micro_services.base import RequestMicroService

logger = logging.getLogger(__name__)


def add_qs_param_to_context(context, param_name, param_value):
    state_auth_req_params = context.state.get(Context.KEY_AUTH_REQ_PARAMS) or {}
    context_auth_req_params = context.get_decoration(Context.KEY_AUTH_REQ_PARAMS) or {}
    state_auth_req_params[param_name] = param_value
    context_auth_req_params[param_name] = param_value
    context.state[Context.KEY_AUTH_REQ_PARAMS] = state_auth_req_params
    context.decorate(Context.KEY_AUTH_REQ_PARAMS, context_auth_req_params)


class SendRequesterClientID(RequestMicroService):
    """
    This SATOSA microservice should be used
    when this proxy's backend is connected to another proxy.
    It reads the current requester ID
    and puts it into a query parameter for next authentication.
    """

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("SendRequesterClientID is active")

        self.__param_name = config.get("param_name", "requester_client_id")

    def process(self, context: Context, data: InternalData):
        add_qs_param_to_context(context, self.__param_name, data.requester)

        return super().process(context, data)


class ForwardRequesterClientID(RequestMicroService):
    """
    This SATOSA microservice should be used
    when this proxy's frontend is connected to another proxy.
    It reads requester client ID from a query parameter
    and puts it into state for the SAML backend to send as SAML requester ID.
    """

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("ForwardRequesterClientID is active")

        self.__param_name = config.get("param_name", "requester_client_id")

    def process(self, context: Context, data: InternalData):
        if self.__param_name in context.qs_params:
            context.state[STATE_KEY_BASE]["requester"] = context.qs_params[
                self.__param_name
            ]

        return super().process(context, data)
