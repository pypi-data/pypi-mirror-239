import warnings

warnings.warn("ixoncdkingress.cbc had been deprecated, please use ixoncdkingress.function", DeprecationWarning)

from ixoncdkingress.function.document_db_client import TIMEOUT, DocumentType, DocumentDBAuthentication, DocumentDBClient
