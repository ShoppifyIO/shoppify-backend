create or replace function
    guard_shopping_list()
returns trigger as
$BODY$
begin
    if not exists (select 1 from users where id = new.owner_id) then
        perform throw.user_not_found();
    end if;

    if new.category_id is not null and not exists (select 1 from categories where id = new.category_id) then
        perform throw.category_not_found();
    end if;

    if check_is_length_too_long(new.title, 200) then
        perform throw.shopping_list_title_too_long();
    end if;

    return new;
end;
$BODY$
language plpgsql;

create or replace function
    delete_sharings_on_delete()
returns trigger as
$BODY$
begin
    DELETE FROM shopping_list_items WHERE shopping_list_id = old.id;
    DELETE FROM list_sharings WHERE shopping_list_id = old.id;

    return old;
end;
$BODY$
language plpgsql;

create or replace trigger delete_sharings_on_delete_list
    before delete on shopping_lists
    for each row execute procedure delete_sharings_on_delete();

create or replace trigger guard_shopping_list_insert
    before insert on shopping_lists
    for each row execute procedure guard_shopping_list();

create or replace trigger guard_shopping_list_update
    before update on shopping_lists
    for each row execute procedure guard_shopping_list();

create or replace trigger fill_update_fields
    before update on shopping_lists
    for each row execute procedure fill_update_date();