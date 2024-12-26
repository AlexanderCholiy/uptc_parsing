def select_messages_details_urls(
    personal_area_id: int, declarant_id: int
) -> str:
    return (f'''
    SELECT
        ms.message_number,
        mc.constant_text
    FROM
        messages as ms LEFT JOIN messages_constants as mc
        ON ms.id = mc.message_id
    WHERE
        mc.constant_type = 1040
        AND mc.constant_text IS NOT NULL
        AND ms.personal_area_id = {personal_area_id}
        AND ms.declarant_id = {declarant_id}
    ''')
