create or replace function
    check_is_length_too_long(
        p_text text,
        p_max_length integer
    )
returns boolean as $$
begin
    if length(p_text) > p_max_length then
        return true;
    end if;

    return false;
end;
$$ language plpgsql;
