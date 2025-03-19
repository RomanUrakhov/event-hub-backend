from apiflask import Schema, fields


class EventAccessSchema(Schema):
    can_enroll_streamers = fields.Boolean(required=True)
    can_moderate_highlights = fields.Boolean(required=True)


class AccountAccessSchema(Schema):
    global_access = fields.Boolean(required=True, description="Global access status")
    events = fields.Dict(
        fields.String,
        fields.Nested(EventAccessSchema),
        required=True,
        description="Mapping of event IDs to access details. Each key represents an `event_id`.",
        example={
            "event_123": {
                "can_enroll_streamers": True,
                "can_moderate_highlights": False,
            },
            "event_456": {
                "can_enroll_streamers": False,
                "can_moderate_highlights": True,
            },
        },
    )


class AccountAccessQueryParams(Schema):
    event_id = fields.String(required=False, description="Filter access by Event ID")
