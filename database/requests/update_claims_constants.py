from datetime import datetime


def request_update_claims_constants(
    personal_area_id: int, declarant_id: int, claim_number: str,
    parsing_data: datetime, constant_type: int, constant_text: str
) -> str:
    """Обновление таблицы constants"""
    return (f"""
    DO $$
    DECLARE
        v_claim_id INT;
    BEGIN
        -- Получаем claim_id
        SELECT id INTO v_claim_id
        FROM claims
        WHERE
            claim_number = '{claim_number}'
            AND personal_area_id = {personal_area_id}
            AND declarant_id = {declarant_id}
        LIMIT 1;

        -- Проверяем, была ли найдена запись
        IF v_claim_id IS NULL THEN
            -- Завершаем выполнение блока, если запись не найдена
            RAISE EXCEPTION 'Запись не найдена для claim_number = ''{(
                claim_number
        )}''';
        END IF;

        -- Попытка обновить запись:
        UPDATE constants
        SET
            constant_text = '{constant_text}',
            time_stamp = '{parsing_data}'
        WHERE
            claim_id = v_claim_id
            AND constant_type = {constant_type};

        -- Проверка, была ли обновлена запись:
        IF NOT FOUND THEN
            -- Если не было обновлено, вставляем новую запись:
            INSERT INTO constants (
                claim_id, constant_type, constant_text, time_stamp
            )
            VALUES (
                v_claim_id,
                {constant_type},
                '{constant_text}',
                '{parsing_data}'
            );
        END IF;
    END $$;
    """)
