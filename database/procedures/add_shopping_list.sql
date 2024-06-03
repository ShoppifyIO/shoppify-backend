create or replace function
    add_shopping_list(
        p_owner_id integer,
        p_title text,
        p_category_id integer default null
    )
returns integer as $$
declare
    v_shopping_list_id integer;
begin
    insert into shopping_lists (owner_id, title, category_id)
    values (p_owner_id, p_title, p_category_id)
    returning id into v_shopping_list_id;

    return v_shopping_list_id;
end;
$$ language plpgsql;
