from enum import Enum, auto
import logging


class BaseMessage(Enum):
    def format(self, level, **kwargs):
        """
        It appends PAIG-5x as logging.ERROR is 50
        :param kwargs:
        :return: formatted string with PAIG-5x prefix
        """
        return f'{logging.getLevelName(level)}: PAIG-{level}{str(self.value[0]).zfill(4)}: {self.value[1].format(**kwargs)}'


class ErrorMessage(BaseMessage):
    """
    Enum that has all the error messages. Do not change the order of the messages. Add new message to the end of the
    list always so that the order is not changed.
    """
    TENANT_ID_NOT_PROVIDED = auto(), "Tenant ID is not provided"
    API_KEY_NOT_PROVIDED = auto(), "API Key is not provided. " \
                                   "You can pass it as a parameter or use the 'api_key_provider' option " \
                                   "or set the 'PAIG_API_KEY' environment variable."
    PAIG_IS_ALREADY_INITIALIZED = auto(), "The PAIG plugin is already initialized"
    PAIG_ACCESS_DENIED = auto(), "Access denied. Server returned error-code={error_code}, error-message={error_message}"
    FRAMEWORKS_NOT_PROVIDED = auto(), "Frameworks are not provided. You should provide at least one framework such as " \
                                      "langchain. You can set to None if you don't want to intercept any framework."
    SHIELD_SERVER_KEY_ID_NOT_PROVIDED = auto(), "Shield server key id is not provided"
    SHIELD_SERVER_PUBLIC_KEY_NOT_PROVIDED = auto(), "Shield server public key is not provided"
    SHIELD_PLUGIN_KEY_ID_NOT_PROVIDED = auto(), "Shield plugin key id is not provided"
    SHIELD_PLUGIN_PRIVATE_KEY_NOT_PROVIDED = auto(), "Shield plugin private key is not provided"
    SHIELD_SERVER_INITIALIZATION_FAILED = auto(), "Shield server initialization failed"

    def format(self, **kwargs):
        return super().format(logging.ERROR, **kwargs)


class InfoMessage(BaseMessage):
    """
    Enum that has all the info messages. Do not change the order of the messages. Add new message to the end of the
    list always so that the order is not changed.
    """
    PAIG_IS_INITIALIZED = auto(), "PAIGPlugin initialized with {kwargs}"
    LANGCHAIN_INITIALIZED = auto(), "Langchain setup done with {count} methods intercepted"
    NO_FRAMEWORKS_TO_INTERCEPT = auto(), "No frameworks to intercept"
    PRIVACERA_SHIELD_IS_ENABLED = auto(), "Privacera Shield, enabled={is_enabled}"

    def format(self, **kwargs):
        return super().format(logging.INFO, **kwargs)


class WarningMessage(BaseMessage):
    """
    Enum that has all the warning messages. Do not change the order of the messages. Add new message to the end of the
    list always so that the order is not changed.
    """
    ERROR_MESSAGE_CONFIG_FILE_NOT_FOUND = auto(), "Error message config file not found at {file_path}"
    FRAMEWORK_NOT_SUPPORTED = auto(), "Framework {framework} is not supported"

    def format(self, **kwargs):
        return super().format(logging.WARNING, **kwargs)
