create or replace function
    guard_shopping_list()
returns trigger as
$BODY$
begin
    if not exists (select 1 from users where id = new.owner_id) then
        perform throw.user_not_found();
    end if;

    if not exists (select 1 from categories where id = new.category_id) then
        perform throw.category_not_found();
    end if;

    if check_is_length_too_long(new.title, 200) then
        perform throw.shopping_list_title_too_long();
    end if;

    return new;
end;
$BODY$
language plpgsql;

create or replace trigger guard_shopping_list
    before insert on shopping_lists
    for each row execute procedure guard_shopping_list();

create or replace trigger guard_shopping_list
    before update on shopping_lists
    for each row execute procedure guard_shopping_list();

create or replace trigger fill_update_fields
    before update on shopping_lists
    for each row execute procedure fill_update_date();