drop table if exists
    list_sharings,
    user_relationships,
    shopping_list_items,
    shopping_lists,
    user_items,
    categories,
    users;

drop function if exists public.

drop function if exists
    add;
    add_user,
    check_is_length_too_long,
    check_is_null_or_empty,
    fill_update_date,
    guard_shopping_list;

