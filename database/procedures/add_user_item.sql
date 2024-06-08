create or replace function
    add_user_item(
        p_user_id integer,
        p_category_id integer,
        p_name text
    )
returns integer as $$
declare
    v_user_item_id integer;
begin
    perform public.verify_user_exists(p_user_id);
    perform public.verify_category_exists(p_category_id, p_user_id, true);

    insert into user_items (owner_id, category_id, name)
    values (p_user_id, p_category_id, p_name)
    returning id into v_user_item_id;

    return v_user_item_id;
end;
$$ LANGUAGE plpgsql VOLATILE;
