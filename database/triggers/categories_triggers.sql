create or replace function
    clear_category_from_objects()
returns trigger as
$BODY$
begin
    if old.type = 1 then
        update shopping_lists set category_id = null where category_id = old.id;
    end if;

    if old.type = 2 then
        update shopping_list_items set category_id = null where category_id = old.id;
        update user_items set category_id = null where category_id = old.id;
    end if;

    return old;
end;
$BODY$
language plpgsql;

create or replace trigger clear_category_from_objects
    before delete on categories
    for each row execute procedure clear_category_from_objects();