create or replace function
    login(
        p_username varchar,
        p_password varchar
    )
returns void as $$
declare
    v_password_hash text;
begin
    v_password_hash := crypt(p_password, gen_salt('bf'));

    if not exists(select 1 from users where username = p_username and password_hash = v_password_hash) then
        perform throw.username_or_password_incorrect();
    end if;

    raise notice 'User can be logged in';
end;
$$ language plpgsql;

comment on function login(varchar, varchar) is
'Możliwe wyjątki:
- U007 - Username or password is incorrect';
