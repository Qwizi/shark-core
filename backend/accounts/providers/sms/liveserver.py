from accounts.providers.sms.provider import AbstractSMSProvider


class LiveServerSMSProvider(AbstractSMSProvider):
    tag = 'liveserver'
