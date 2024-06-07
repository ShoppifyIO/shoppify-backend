create or replace function throw.shopping_list_title_too_long() returns void as $$
begin raise exception 'Za długi tytuł listy zakupów' using errcode = 'S0001'; end;
$$ language plpgsql;

create or replace function throw.cannot_share_with_non_friend() returns void as $$
begin raise exception 'Nie można udostępniać listy osobom, które nie są przyjaciółmi' using errcode = 'S0002'; end;
$$ language plpgsql;

create or replace function throw.cannot_share_non_owned_list() returns void as $$
begin raise exception 'Nie można udostępniać listy nie będąc jej właścicielem' using errcode = 'S0003'; end;
$$ language plpgsql;