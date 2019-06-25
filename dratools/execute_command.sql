create or replace function execute_command(command character varying)
    returns TABLE
            (
                command_output text
            )
    language plpgsql
as
$$
BEGIN
    CREATE TEMP TABLE temp_table
    (
        command_output text
    );
--    COPY temp_table FROM PROGRAM 'du -hs *';
    EXECUTE format('COPY temp_table FROM PROGRAM ''%s'' WITH (FORMAT text, DELIMITER %L)', command || '| tr -d ^', '^');


    RETURN QUERY
        SELECT *
        from temp_table;

    DROP TABLE temp_table;

END;
$$;

alter function execute_command(varchar) owner to current_user;