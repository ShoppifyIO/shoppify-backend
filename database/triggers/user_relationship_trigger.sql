create or replace function
    guard_insert_relationship()
returns trigger as
$BODY$
begin
    if exists (select 1 from user_relationships where user_1_id = new.user_1_id and user_2_id = new.user_2_id) then
        perform throw.relationship_already_exists();
    end if;

    if exists (select 1 from user_relationships where user_1_id = new.user_2_id and user_2_id = new.user_1_id) then
        perform throw.relationship_already_exists();
    end if;

    return new;
end;
$BODY$
language plpgsql;

create or replace function
    forbid_relationship_modification()
returns trigger as
$BODY$
begin
    perform throw.relationship_cannot_be_modified();
end;
$BODY$
language plpgsql;

create or replace trigger guard_relationship_insert
    before insert on user_relationships
    for each row execute procedure guard_insert_relationship();

create or replace trigger guard_relationship_update
    before update on user_relationships
    for each row execute procedure forbid_relationship_modification();
