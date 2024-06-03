create or replace function
    fill_update_date()
returns trigger as
$BODY$
begin
    new.update_date = now();
    return new;
end;
$BODY$
language plpgsql;