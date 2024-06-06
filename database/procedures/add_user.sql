create or replace function
    add_user(
        p_username text,
        p_email text,
        p_password text
    )
returns integer as $$
declare
    v_password_hash text;
    v_user_id integer;
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
    values (p_username, p_email, v_password_hash, true)
    returning id into v_user_id;

    raise notice 'User added successfully';

    return v_user_id;
end
$$ language plpgsql;

comment on function add_user(text, text, text) is
'Możliwe wyjątki:
- U001 - Username already taken
- U002 - Email already taken
- U003 - Username is empty
- U004 - Email is empty
- U005 - Username is too long
- U006 - Email is too long';


create or replace function
    add_friend(
        p_asking_user_id integer,
        p_asked_user_id integer
    )
returns void as $$
begin

    insert into user_relationships(user_1_id, user_2_id)
    values (p_asking_user_id, p_asked_user_id);

    raise notice 'Friend added successfully';
end
$$ language plpgsql;
