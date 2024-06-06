create or replace function throw.username_taken() returns void AS $$
begin raise exception 'Username already taken' using errcode = 'U0001'; end;
$$ language plpgsql;

create or replace function throw.email_taken()returns void AS $$
begin raise exception 'Email already taken' using errcode = 'U0002'; end;
$$ language plpgsql;

create or replace function throw.empty_username() returns void AS $$
begin raise exception 'Username is empty' using errcode = 'U0003'; end;
$$ language plpgsql;

create or replace function throw.empty_email() returns void AS $$
begin raise exception 'Email is empty' using errcode = 'U0004'; end;
$$ language plpgsql;

create or replace function throw.username_too_long() returns void AS $$
begin raise exception 'Username is too long' using errcode = 'U0005'; end;
$$ language plpgsql;

create or replace function throw.email_too_long() returns void AS $$
begin raise exception 'Email is too long' using errcode = 'U0006'; end;
$$ language plpgsql;

create or replace function throw.username_or_password_incorrect() returns void AS $$
begin raise exception 'Username or password is incorrect' using errcode = 'U0007'; end;
$$ language plpgsql;

create or replace function throw.user_not_found() returns void as $$
begin raise exception 'Nie znaleziono podanego użytkownika' using errcode = 'U0008'; end;
$$ language plpgsql;

create or replace function throw.relationship_already_exists() returns void as $$
begin raise exception 'Już jesteś znajomy z tym użytkownikiem' using errcode = 'U0009'; end;
$$ language plpgsql;

create or replace function throw.relationship_cannot_be_modified() returns void as $$
begin raise exception 'Już jesteś znajomy z tym użytkownikiem' using errcode = 'U0010'; end;
$$ language plpgsql;
