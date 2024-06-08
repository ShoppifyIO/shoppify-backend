create or replace function
    add_shopping_item(
        p_shopping_list_id integer,
        p_name text,
        p_added_by integer,
        p_quantity integer default null,
        p_category_id integer default null
    )
returns integer as $$
declare
    v_shopping_item_id integer;
begin
    insert into shopping_list_items (shopping_list_id, name, quantity, added_by, category_id)
    values (p_shopping_list_id, p_name, p_quantity, p_added_by, p_category_id)
    returning id into v_shopping_item_id;

    return v_shopping_item_id;
end;
$$ LANGUAGE plpgsql VOLATILE;


