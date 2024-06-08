create or replace function
    add_shopping_list(
        p_owner_id integer,
        p_title text,
        p_category_id integer default null
    )
returns integer as $$
declare
    v_shopping_list_id integer;
begin
    insert into shopping_lists (owner_id, title, category_id)
    values (p_owner_id, p_title, p_category_id)

    returning id into v_shopping_list_id;

    return v_shopping_list_id;
end;
$$ language plpgsql;

create or replace function
    share_shopping_list(
        p_user_id integer,
        p_friend_id integer,
        p_shopping_list_id integer
    )
returns void as $$
declare
    v_relationship_id integer;
    v_relationship_id_1 integer;
    v_relationship_id_2 integer;
begin
    if not exists (select 1 from shopping_lists where id = p_shopping_list_id and owner_id = p_user_id) then
        perform throw.cannot_share_non_owned_list();
    end if;

    select id into v_relationship_id_1
    from user_relationships
    where user_1_id = p_user_id and user_2_id = p_friend_id;

    select id into v_relationship_id_2
    from user_relationships
    where user_1_id = p_friend_id and user_2_id = p_user_id;

    if v_relationship_id_1 is not null then
        v_relationship_id := v_relationship_id_1;
    end if;

    if v_relationship_id_2 is not null then
        v_relationship_id := v_relationship_id_2;
    end if;

    if v_relationship_id is null then
        perform throw.cannot_share_with_non_friend();
    end if;

    insert into list_sharings(user_relationship_id, shopping_list_id, permission_level)
    values (v_relationship_id, p_shopping_list_id, 1);

    raise notice 'Successfully shared shopping list';
end
$$ LANGUAGE plpgsql VOLATILE;
