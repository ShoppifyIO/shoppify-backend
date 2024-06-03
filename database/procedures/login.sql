create or replace function
    login(
        p_username varchar,
        p_password varchar
    )
returns table(
    v_user_id integer,
    v_username varchar,
    v_email varchar
) as $$
declare
    v_password_hash text;
begin
    select id, username, email, password_hash into v_user_id, v_username, v_email, v_password_hash
    from users
    where username = p_username;

    if v_user_id is null or v_password_hash != crypt(p_password, v_password_hash) then
        perform throw.username_or_password_incorrect();
    end if;

    return query
    select v_user_id, v_username, v_email;
end;
$$ language plpgsql;

comment on function login(varchar, varchar) is
'Możliwe wyjątki:
- U007 - Username or password is incorrect';
