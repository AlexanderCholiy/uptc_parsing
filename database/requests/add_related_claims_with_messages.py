from typing import Optional


def add_related_claims_with_messages(
    personal_area_id: Optional[int] = None, declarant_id: Optional[int] = None
) -> str:
    personal_area_id_filter = (
        f'AND cl.personal_area_id = {personal_area_id}'
    ) if personal_area_id is not None else ''
    declarant_id_filter = (
        f'AND cl.declarant_id = {declarant_id}'
    ) if declarant_id is not None else ''

    return (f'''
    INSERT INTO messages_constants (
        message_id,
        constant_type,
        constant_text,
        time_stamp
    )
    SELECT DISTINCT
        mc.message_id,
        2070 AS constant_type,
        cl.claim_number AS constant_text,
        mc.time_stamp
    FROM messages_constants mc
    LEFT JOIN claims cl ON mc.constant_text LIKE '%' || cl.claim_number || '%'
    WHERE
        mc.constant_type = 2060
        AND cl.claim_number IS NOT NULL
        {personal_area_id_filter}
        {declarant_id_filter}
        AND NOT EXISTS (
            SELECT 1
            FROM messages_constants AS mc2
            WHERE
                mc2.message_id = mc.message_id
                AND mc2.constant_type = 2070
                AND mc2.constant_text = cl.claim_number
        )
        AND NOT EXISTS (
            SELECT 1
            FROM messages_constants AS mc3
            WHERE
                mc3.message_id = mc.message_id
                AND mc3.constant_type = 2070
        );
    '''.strip())
