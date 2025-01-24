def select_claims_details_urls(
    personal_area_id: int, declarant_id: int
) -> str:
    return (f'''
    SELECT DISTINCT
        cl.claim_number,
        cc.constant_text
    FROM
        claims as cl INNER JOIN constants as cc
        ON cl.id = cc.claim_id
    WHERE
        cc.constant_type = 1040
        AND cc.constant_text IS NOT NULL
        AND cl.personal_area_id = {personal_area_id}
        AND cl.declarant_id = {declarant_id}
    ''')
