class AppMessages:
    # Class to store constant messages
    MAIL_NOT_VERIFY = 'Account is not verify. Please check your email for verification link.'
    INVALID_LOGIN_CREDENTIALS = 'Invalid email or password.'
    INTERNAL_SERVER_ERROR = 'Internal server error.'
    VERIFY_EMAIL_SENT = 'A verification link have been sent to your email.'
    EMAIL_EXIST = 'Email already have an account registered'
    RESET_EMAIL_SENT = 'A password reset link have been sent to your email'
    INVALID_EMAIL = 'Invalid email.'
    SIGN_OUT = 'You have successfully signed out.'
    ACCOUNT_DELETED = 'You have successfully deleted your account.'
    GSHEET_CONNECTION_ERROR = 'GoogleSheetAPI connection error.'
    WARNING_CHANGES_NOT_SAVED = 'Changes you made have not been saved.'
    WARNING_SHEET_EMPTY = 'Sheet is empty.'
    VALIDATION_ERROR_MISSING = 'EMPTY_OR_MISSING'
    VALIDATION_EXPENSE_TYPE = 'EXPENSE_TYPE_INPUT'
    VALIDATION_DATE = 'DATE_INPUT'
    VALIDATION_ERROR_OOB = 'OUT_OF_BOUND'

    
    
    @staticmethod
    def get_connecition_errors(args):
        return "Connection error: "+"-".join(args)
    @staticmethod
    def get_validation_errors(args):
        return "Input error: "+":".join(args)