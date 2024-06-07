create or replace function
    set_completion_date()
returns trigger as
$BODY$
begin
    if new.is_completed and not old.is_completed then
        new.completion_date = now();
    end if;

    if not new.is_completed and old.is_completed then
        new.completion_date = null;
        new.completed_by = null;
    end if;

    return new;
end;
$BODY$
language plpgsql;

create or replace trigger set_completion_date
    before update on shopping_list_items
    for each row execute procedure set_completion_date();