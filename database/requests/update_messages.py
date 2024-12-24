def request_update_messages(
    personal_area_id: int, declarant_id: int, message_number: str
) -> str:
    """Добавление новых обращений в messages"""
    return (f"""
    INSERT INTO messages (
        declarant_id,
        personal_area_id,
        message_number
    )
    SELECT
        {declarant_id}, {personal_area_id}, '{message_number}'
    WHERE
        NOT EXISTS (
            SELECT 1 FROM messages
            WHERE
                message_number = '{message_number}'
                AND declarant_id = {declarant_id}
                AND personal_area_id = {personal_area_id}
            LIMIT 1
        );
    """)
