CREATE OR REPLACE PROCEDURE insert_many_contacts(
    names TEXT[],
    phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP

        IF phones[i] !~ '^\+\d{10,15}$' THEN
            RAISE NOTICE 'Invalid phone: %', phones[i];
        ELSE
            INSERT INTO contacts(first_name, phone)
            VALUES (names[i], phones[i])
            ON CONFLICT (phone) DO NOTHING;
        END IF;

    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE first_name ILIKE '%' || value || '%'
       OR last_name ILIKE '%' || value || '%'
       OR phone ILIKE '%' || value || '%';
END;
$$;

CREATE OR REPLACE PROCEDURE upsert_contact(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO contacts (first_name, phone)
    VALUES (p_name, p_phone)
    ON CONFLICT (phone)
    DO UPDATE SET first_name = EXCLUDED.first_name;
END;
$$;