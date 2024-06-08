create or replace function
    public.verify_user_exists(
        p_user_id integer
    )
returns void as $$
begin
    if not exists(select 1 from users where id = p_user_id) then
        perform throw.user_not_found();
    end if;
end;
$$ language plpgsql;

create or replace function
    public.verify_category_exists(
        p_category_id integer,
        p_user_id integer,
        p_allow_null boolean
    )
returns void as $$
begin
    if p_category_id is null and p_allow_null then
        return;
    end if;

    if not exists(select 1 from categories where id = p_category_id and owner_id = p_user_id) then
        perform throw.category_not_found();
    end if;
end;
$$ language plpgsql;