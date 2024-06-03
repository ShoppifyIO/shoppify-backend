create or replace function
    check_is_null_or_empty(
        p_text text
    )
returns boolean as $$
begin
    if p_text is null or p_text = '' then
        return true;
    end if;

    return false;
end;
$$ language plpgsql;