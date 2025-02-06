# classes/messages.py

import gettext
import streamlit as st

# Set the locale directory and domain
#msgfmt locales/vi/LC_MESSAGES/messages.po -o locales/vi/LC_MESSAGES/messages.mo
#msgfmt locales/en/LC_MESSAGES/messages.po -o locales/en/LC_MESSAGES/messages.mo


class AppMessages:
    # Set the default language
    def __init__(self,language):
        self.domain = 'messages'
        self.language =language
    # Function to set the language
        locale_path = "./locales"
        gettext.bindtextdomain(self.domain, locale_path)
        gettext.textdomain(self.domain)
        lang = gettext.translation(self.domain, localedir=locale_path, languages=[self.language], fallback=True)
        lang.install()
        self._ = lang.gettext
        # Notification messages
        _ = self._
        self.MAIL_NOT_VERIFY = _('Account is not verify. Please check your email for verification link.')
        self.INVALID_LOGIN_CREDENTIALS = _('Invalid email or password.')
        self.INTERNAL_SERVER_ERROR = _('Internal server error.')
        self.VERIFY_EMAIL_SENT = _('A verification link have been sent to your email.')
        self.EMAIL_EXIST = _('Email already have an account registered')
        self.RESET_EMAIL_SENT = _('A password reset link have been sent to your email')
        self.INVALID_EMAIL = _('Invalid email.')
        self.INVALID_LOGIN_CODE = _('Invalid sign in code.')
        self.SIGN_OUT = _('You have successfully signed out.')
        self.ACCOUNT_DELETED = _('You have successfully deleted your account.')
        self.GSHEET_CONNECTION_ERROR = _('GoogleSheetAPI connection error.')
        self.WARNING_CHANGES_NOT_SAVED = _('Changes you made have not been saved.')
        self.WARNING_SHEET_EMPTY = _('No Entries.')
        self.INVALID_DATE = _('Please choose a start/end date.')
        self.INVALID_EXPENSE_TYPE = _('Please choose an expense type.')
        self.SENDING_RESET_EMAIL = _('Sending password reset email')
        self.SENDING_SIGNUP_EMAIL = _('Sending confirmation email')
        self.WEAK_PASSWORD = _('Weak Password. Password must contain: ')
        # Buttons
        self.INSERT_BUTTON = _('Insert')
        self.UPDATE_BUTTON = _('Edit')
        self.EXPORT_BUTTON = _('Export')
        self.SAVE_BUTTON = _('Save')
        self.SIGN_IN_GOOGLE = _('Sign in with Google')
        self.SIGN_IN = _('Sign In')
        self.CREATE_ACCOUNT = _('Create Account')
        self.FORGET_PASSWORD = _('Forget Password')
        self.SEND_BUTTON = _('Send')
        self.LOGOUT_BUTTON = _("Logout")
        # Form
        self.INSERT_FORM = _('Insert Data')
        self.UPDATE_FORM = _('Edit Data')
        self.EXPORT_FORM = _('Export Data')
        self.SIGN_IN_FORM = _('Sign in')
        self.CREATE_ACCOUNT_FORM = _('Create your account')
        self.FORGET_PASSWORD_FORM = _('Reset password')
        # Text
        self.APP_DESCRIPTION = _("A user-friendly Streamlit app designed to streamline your financial management. By seamlessly store data to Google Sheets, it allows you to track expenses, manage budgets, and generate insightful financial reports. With intuitive visualizations, the app helps you stay on top of your finances effortlessly.")
        self.FUNCTION_DESCRIPTIONS = _("Functions")
        self.FUNCTION_CARDS_DESCRIPTION =_("Below are the cards explaining what each of the functions are.")
        self.EXPANDER = _("Expand")
        self.UTIL_DESCRIPTION = _("Utilities")
        # Description
        self.DESC_DASHBOARD = _("Metrics, charts from your expenses reports.")
        self.DESC_BUG = _("Report bugs in our github repo's issue page.")
        self.DESC_REPO = _("Source code of the project is found here.")
        self.DESC_MENU = _("Navigation menu.")
        self.DESC_LOGOUT = _("Logout.")
        self.DESC_LANG_SWITCH = _("Language.")
        # Tooltip
        self.AMOUNT_TOOLTIP = _("Amount should be in VND")
        self.AMOUNT_TOOLTIP_NAME = _("Amount")
        
        self.TYPE_TOOLTIP_NAME = _("Type of Expense")
        self.OTHER_TYPE_TOOLTIP_NAME = _("Input another type: ")
        
        self.NOTE_TOOLTIP = _("Input note here...")
        self.NOTE_TOOLTIP_NAME = _("Notes")
        self.DATEINPUT_TOOLTIP_NAME = _("Document Date:")
        
        self.WEEK_TOOLTIP = _("Week")
        self.DAY_OF_WEEK_TOOLTIP = _("Day of Week")
        self.WEEK_OF_MONTH_TOOLTIP = _("Week of Month")
        self.MONTH_TOOLTIP = _("Month")
        self.YEAR_TOOLTIP = _("Year")
        
        self.SPAN_TOOLTIP_NAME= _("Select your expense span")
        self.SPAN_TOOLTIP = _("First entry:")
        
        self.TOTAL_SPENDING_TOOLTIP =_("Total Spending (VND)")
        self.HIGHEST_SPENDING_TOOLTIP =_("Highest Spending (VND)")
        
        self.RELOAD_APP_TOOLTIP = _("Reload the app.")
        self.OLD_METRIC_TOOLTIP = _("Old")
        
        self.EXPORT_TOGGLE_TOOLTIP = _("Download the full sheet ?")
        self.EXPORT_TYPE_TOOLTIP = _("Default type: .csv")
        self.EXPORT_TYPE_TOOLTIP_NAME =_("File Type")
        
        self.SIGN_IN_TOOLTIP = _('Already have an account ?')
        self.SIGN_IN_LOAD_TOOLTIP = _('Signing in...')
        
        self.PASSWORD_TOOLTIP = _("Password")
        self.LOADING_TOOLTIP = _('Loading...')
        # Tab names
        self.METRICS = _("Metrics")
        self.HEAT_MAP = _("Spending Map Chart")
        self.LINE_CHART = _("Line Chart")
        self.BAR_CHART = _("Bar Chart")
        self.PIE_CHART = _("Pie Chart")
        self.DATA_FRAME = _("Dataframe")
        
    def get_comparestring(self,last,current):
        tmp = self._("Metrics only compare from current month - last month")
        msg =f"""{tmp} (`{current}` - `{last}`)"""
        return msg
    
    def get_connection_errors(self,args):
        return self._("Connection error: ") + "-".join(args)

    def get_validation_errors(self,args):
        return self._("Input error: ") + ":".join(args)
