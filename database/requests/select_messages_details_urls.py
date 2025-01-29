def select_messages_details_urls(
    personal_area_id: int, declarant_id: int, check_constant_type: int
) -> str:
    return (f'''
    SELECT DISTINCT
        ms.message_number,
        mc.constant_text
    FROM
        messages as ms INNER JOIN messages_constants as mc
        ON ms.id = mc.message_id
    WHERE
        mc.constant_type = 1040
        AND mc.constant_text IS NOT NULL
        AND ms.personal_area_id = {personal_area_id}
        AND ms.declarant_id = {declarant_id}
        AND mc.message_id NOT IN (
            SELECT
                mc.message_id
            FROM
                messages as ms INNER JOIN messages_constants as mc
                ON ms.id = mc.message_id
            WHERE
                mc.constant_type = {check_constant_type}
                AND mc.constant_text IS NOT NULL
                AND ms.personal_area_id = {personal_area_id}
                AND ms.declarant_id = {declarant_id}
        )
    ''')
