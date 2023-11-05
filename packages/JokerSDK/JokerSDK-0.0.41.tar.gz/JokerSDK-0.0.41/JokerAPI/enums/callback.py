from uuid import uuid4
from hashlib import sha256
from strenum import StrEnum

class Enums(StrEnum):
    RINGING = "call.ringing"
    ANSWERED = "call.answered"
    HANGUP = "call.ended"
    ENDED = "call.ended"

    DTMF_GATHERED = "dtmf.gathered"
    DTMF_RECIEVED = "Single DTMF"

    VOICEMAIL_DETECTED = "machine.detected"
    HUMAN_DETECTED = "human.detected"
    NOTSURE_DETECTED = "notsure.detected"