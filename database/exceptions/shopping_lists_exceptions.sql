create or replace function throw.shopping_list_title_too_long() returns void as $$
begin raise exception 'Za długi tytuł listy zakupów' using errcode = 'S0001'; end;
$$ language plpgsql;