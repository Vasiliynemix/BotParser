from aiogram.filters.callback_data import CallbackData


class CallbackWebsiteFilter(CallbackData, prefix="callback_text"):
    call_text: str
