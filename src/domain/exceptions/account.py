class AccountDoesNotHaveAccessException(Exception):
    def __init__(self, account_id, event_id) -> None:
        self.account_id = account_id
        self.event_id = event_id
        super().__init__(
            f"User account {self.account_id} doesn't have sufficient access to event {event_id}"
        )


class AccountDoesNotHaveCreatorAccessException(Exception):
    def __init__(self, account_id: str) -> None:
        self.account_id = account_id
        super().__init__(
            f"User account {self.account_id} doesn't have sufficient access to create events"
        )
