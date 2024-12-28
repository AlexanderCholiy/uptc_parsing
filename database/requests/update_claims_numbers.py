def request_update_claims_numbers(
    personal_area_id: int, declarant_id: int, claim_number: str
) -> str:
    """Добавление новых заявок в claims"""
    return (f"""
    INSERT INTO claims (
        declarant_id,
        personal_area_id,
        claim_number
    )
    SELECT
        {declarant_id}, {personal_area_id}, '{claim_number}'
    WHERE
        NOT EXISTS (
            SELECT 1 FROM claims
            WHERE
                claim_number = '{claim_number}'
                AND declarant_id = {declarant_id}
                AND personal_area_id = {personal_area_id}
        );
    """)
