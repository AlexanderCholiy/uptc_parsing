from datetime import datetime


def request_update_claims_states(
    personal_area_id: int, declarant_id: int, claim_number: str,
    claim_status: str, parsing_data: datetime
) -> str:
    """Добавление уникальных статусов в claims_states."""
    return (f"""
    INSERT INTO claims_states (
        claim_id,
        claim_status,
        time_stamp
    )
    SELECT (
        SELECT id FROM claims
        WHERE
            claim_number = ('{claim_number}')
            AND declarant_id = {declarant_id}
            AND personal_area_id = {personal_area_id}
        LIMIT 1
    ),
    '{claim_status}',
    '{parsing_data}'
    WHERE
        NOT EXISTS (
            SELECT 1 FROM claims_states
            WHERE
                claim_status = '{claim_status}'
                AND claim_id = (
                    SELECT id FROM claims
                    WHERE claim_number = '{claim_number}'
                    AND personal_area_id = {personal_area_id}
                    AND declarant_id = {declarant_id}
                    LIMIT 1
                )
        );
    """)
