CREATE OR REPLACE FUNCTION add_category(
    p_owner_id integer,
    p_type integer,
    p_title varchar(100),
    p_description varchar,
    p_color char(7)
)
RETURNS integer AS $$
DECLARE
    v_category_id integer;
BEGIN
    INSERT INTO categories (owner_id, type, title, description, color)
    VALUES (p_owner_id, p_type, p_title, p_description, p_color)
    RETURNING id INTO v_category_id;

    RETURN v_category_id;
END;
$$ LANGUAGE plpgsql VOLATILE;


