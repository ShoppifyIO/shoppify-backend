create or replace function
    add_user(
        p_username varchar,
        p_email varchar,
        p_password varchar
    )
returns void as $$
declare
    v_password_hash text;
begin
    if p_username is null or p_username = '' then
        perform throw.empty_username();
    end if;

    if length(p_username) > 50 then
        perform throw.username_too_long();
    end if;

    if p_email is null or p_email = '' then
        perform throw.empty_email();
    end if;

    if length(p_email) > 500 then
        perform throw.email_too_long();
    end if;

    if exists (select 1 from users where username = p_username) then
        perform throw.username_taken();
    end if;

    if exists (select 1 from users where email = p_email) then
        perform throw.email_taken();
    end if;

    v_password_hash := crypt(p_password, gen_salt('bf'));

    insert into users(username, email, password_hash, is_active)
    values (p_username, p_email, v_password_hash, true);

    raise notice 'User added successfully';
end
$$ language plpgsql;

comment on function add_user(varchar, varchar, varchar) is
'Możliwe wyjątki:
- U001 - Username already taken
- U002 - Email already taken
- U003 - Username is empty
- U004 - Email is empty
- U005 - Username is too long
- U006 - Email is too long';
