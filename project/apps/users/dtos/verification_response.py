from dataclasses import dataclass



@dataclass(frozen=True)
class VerificationResponse:
    access_token: str
    refresh_token: str
    message: str

    def to_dict(self):
        return {'message': self.message,
            "data":{
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
        }
    }


@dataclass(frozen=True)
class VerificationResponse:
    access_token: str
    refresh_token: str
    message: str = "Email verified successfully."

    @classmethod
    def from_jwt_dict(cls, jwt_dict):
        return cls(
            access_token=jwt_dict["access"],
            refresh_token=jwt_dict["refresh"]
        )

    def to_dict(self):
        return {'message': self.message,
                "data": {
                    'access_token': self.access_token,
                    'refresh_token': self.refresh_token,
                }
        }



