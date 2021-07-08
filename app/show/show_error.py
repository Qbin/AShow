from common.base_error import BaseError


class ShowError(BaseError):
    # 20XXX show
    SHOW_AUTHENTICATED_EORROR = 20001
    SHOW_NOT_LOGIN = 20002
    SHOW_NOT_FOUND = 20003

    def error(self):
        return {'error': self.errno, 'errmsg': self.message}
