from datetime import datetime


def request_update_messages_states(
    personal_area_id: int, declarant_id: int, message_number: str,
    message_status: str, parsing_data: datetime
):
    """Добавление уникальных статусов в messages_states."""
    return (f"""
    INSERT INTO messages_states (
        message_id,
        message_status,
        time_stamp
    )
    SELECT (
        SELECT id FROM messages
        WHERE
            message_number = ('{message_number}')
            AND declarant_id = {declarant_id}
            AND personal_area_id = {personal_area_id}
        LIMIT 1
    ),
    '{message_status}',
    '{parsing_data}'
    WHERE
        NOT EXISTS (
            SELECT 1 FROM messages_states
            WHERE
                message_status = '{message_status}'
                AND message_id = (
                    SELECT id FROM messages
                    WHERE message_number = '{message_number}'
                    AND personal_area_id = {personal_area_id}
                    AND declarant_id = {declarant_id}
                    LIMIT 1
                )
        );
    """)
