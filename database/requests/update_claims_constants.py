from datetime import datetime


def request_claims_constants_update(
    personal_area_id: int, declarant_id: int, claim_number: str,
    parsing_data: datetime, constant_type: int, constant_text: str
):
    """Обновление таблицы constants"""
    return (f"""
    DO $$
    BEGIN
        -- Попытка обновить запись:
        UPDATE constants
        SET
            constant_text = '{constant_text}',
            time_stamp = '{parsing_data}'
        WHERE
            claim_id = (
                    SELECT id FROM claims
                    WHERE
                        claim_number = '{claim_number}'
                        AND personal_area_id = {personal_area_id}
                        AND declarant_id = {declarant_id}
                    LIMIT 1
                )
            AND constant_type = {constant_type};

        -- Проверка, была ли обновлена запись:
        IF NOT FOUND THEN
            -- Если не было обновлено, вставляем новую запись:
            INSERT INTO constants (
                claim_id, constant_type, constant_text, time_stamp
            )
            VALUES (
                (
                    SELECT id FROM claims
                    WHERE
                        claim_number = '{claim_number}'
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
