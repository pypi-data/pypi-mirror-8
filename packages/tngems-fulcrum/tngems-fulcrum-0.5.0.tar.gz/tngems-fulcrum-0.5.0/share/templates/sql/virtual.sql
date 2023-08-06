{% macro view_proc_wrapper(nspname, relname)%}
-----------------------------------------------------------------------
--  UPDATABLE VIRTUAL RELATION WRAPPER
--
--  Wraps {{ nspname }}.{{ relname }} to make it updatable, and produce
--  nice error messages when an integrity constraint is violated. Note
--  that you still have to declare {{ nspname }}.{{ relname }}__mutate(varchar,
--  varchar[], int, {{ nspname }}.{{ relname }},  {{ nspname }}.{{ relname }})
--  BEFORE including this macro.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION {{ nspname }}.{{ relname }}__mutate()
RETURNS TRIGGER AS
$$
BEGIN
    RETURN {{ nspname }}.{{ relname }}__mutate(TG_OP, TG_ARGV, TG_NARGS,
        TG_TABLE_SCHEMA, TG_TABLE_NAME,
        CASE WHEN TG_OP = 'INSERT' THEN NULL ELSE OLD END,
        CASE WHEN TG_OP = 'DELETE' THEN NULL ELSE NEW END
    );
END;
$$ LANGUAGE PLPGSQL;


DROP TRIGGER IF EXISTS mutate ON {{ nspname }}.{{ relname }} CASCADE;
CREATE TRIGGER mutate
    INSTEAD OF INSERT OR UPDATE OR DELETE
    ON {{ nspname }}.{{ relname }}
    FOR EACH ROW EXECUTE PROCEDURE
    {{ nspname }}.{{ relname }}__mutate();

-----------------------------------------------------------------------
--  End trigger procedure {{ nspname }}.{{ relname }}__mutate()
-----------------------------------------------------------------------
{%- endmacro %}


{% macro view_proc_opening(nspname, relname, schema_state, declare=None, debug=False) %}
-----------------------------------------------------------------------
--  Mutation procedure for {{ nspname }}.{{ relname }}
--
--  A mutation procedure should make the following state changes:
--
--  -   Insert into {{ schema_state }}.{{ relname }}_mutations
--      (if applicable).
--  -   Insert or update the underlying base relations.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION {{ nspname }}.{{ relname }}__mutate(
    TG_OP varchar,
    TG_ARGV varchar[],
    TG_NARGS int,
    TG_TABLE_SCHEMA name,
    TG_TABLE_NAME name,
    OLD {{ nspname }}.{{ relname }},
    NEW {{ nspname }}.{{ relname }}
)
RETURNS {{ nspname }}.{{ relname }} AS
$$
DECLARE
    obj {{ nspname }}.{{ relname }};
{% for varname, datatype in (declare or []) %}
    {{ varname }} {{ datatype }};
{% endfor %}
BEGIN
    -- Bail out early if the record was not changed.
    IF TG_OP = 'UPDATE' AND NEW IS NOT DISTINCT FROM OLD THEN
        RETURN NEW;
    END IF;
    {% if debug %}
    RAISE NOTICE format('Mutating public.principals with mutation timestamp %s',
        public.get_session_mutation_timestamp());
    {% endif %}
    obj := CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
{%- endmacro %}


{% macro view_proc_closing(nspname, relname) %}
    RETURN obj;
END;
$$ LANGUAGE PLPGSQL SECURITY INVOKER;

-----------------------------------------------------------------------
--  End mutation procedure {{ nspname }}.{{ relname }}__mutate()
-----------------------------------------------------------------------
{%- endmacro %}


{% macro view_proc_insert_attrs(nspname, relname, pkname, attrs) %}
{% for attname in attrs %}
--  Insert into {{ nspname }}.{{ relname }}_{{ attname }}
IF NOT public.isempty(NEW.{{ attname }}) THEN
    INSERT INTO {{ nspname }}.{{ relname }}_{{ attname }}
        ({{ pkname|join(',') }}, {{ attname }})
    VALUES
        (NEW.{{ pkname|join(",NEW.") }}, NEW.{{ attname }});
END IF;

{% endfor %}
{% endmacro %}



{% macro view_proc_update_attrs(nspname, relname, pkname, attrs) %}
{% for attname in attrs %}
--  Insert into {{ nspname }}.{{ relname }}_{{ attname }}
IF NEW.{{ attname }} IS DISTINCT FROM OLD.{{ attname }} THEN
    DELETE FROM {{ nspname }}.{{ relname }}_{{ attname }}
    WHERE ({{ pkname|join(',') }}) = (NEW.{{ pkname|join(",NEW.") }});
    INSERT INTO {{ nspname }}.{{ relname }}_{{ attname }}
        ({{ pkname|join(',') }}, {{ attname }})
    VALUES
        (NEW.{{ pkname|join(",NEW.") }}, NEW.{{ attname }});
END IF;

{% endfor %}
{% endmacro %}


{% macro raise_invalid_tg_op() %}
RAISE invalid_parameter_value USING
    MESSAGE = format('Invalid TG_OP: %s', TG_OP),
    HINT = format('Use either INSERT, UPDATE, DELETE or TRUNCATE')
{% endmacro -%}
