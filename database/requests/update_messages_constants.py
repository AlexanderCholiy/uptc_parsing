from datetime import datetime


def request_messages_constants_update(
    personal_area_id: int, declarant_id: int, message_number: str,
    parsing_data: datetime, constant_type: int, constant_text: str
) -> str:
    """Обновление таблицы messages_constants"""
    return (f"""
    DO $$
    BEGIN
        -- Попытка обновить запись:
        UPDATE messages_constants
        SET
            constant_text = '{constant_text}',
            time_stamp = '{parsing_data}'
        WHERE
            message_id = (
                    SELECT id FROM messages
                    WHERE
                        message_number = '{message_number}'
                        AND personal_area_id = {personal_area_id}
                        AND declarant_id = {declarant_id}
                    LIMIT 1
                )
            AND constant_type = {constant_type};

        -- Проверка, была ли обновлена запись:
        IF NOT FOUND THEN
            -- Если не было обновлено, вставляем новую запись:
            INSERT INTO messages_constants (
                message_id, constant_type, constant_text, time_stamp
            )
            VALUES (
                (
                    SELECT id FROM messages
                    WHERE
                        message_number = '{message_number}'
                        AND personal_area_id = {personal_area_id}
                        AND declarant_id = {declarant_id}
                    LIMIT 1
                ),
                {constant_type},
                '{constant_text}',
                '{parsing_data}'
            );
        END IF;
    END $$;
    """)
