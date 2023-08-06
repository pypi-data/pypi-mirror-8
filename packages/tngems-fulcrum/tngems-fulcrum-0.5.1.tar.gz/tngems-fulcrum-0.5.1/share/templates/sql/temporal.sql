{% macro arglist(alias, pk) %}
{% for colname, datatype in pk %}{{ alias }}.{{ colname }}{% if not loop.last %}, {% endif %}{% endfor %}
{% endmacro %}


{% macro argspec(pk) %}
{% for x, datatype in pk %}{{ datatype }}{% if not loop.last %}, {% endif %}{% endfor %}
{% endmacro %}


{% macro columnlist(pk) %}
{% for colname, datatype in pk %}{{ colname }}{% if not loop.last %}, {% endif %}{% endfor %}
{% endmacro %}


{% macro table_mutations(nspname, relname, pk, with_drop=False, cascade=False,
    schema_state="state", schema_domain="common", serial_type="serial",
    schema_entities="entities") -%}
-----------------------------------------------------------------------
--  {{ relname.title() }} Mutation
--
--  Describes a mutation on {{ nspname }}.{{ relname }}.
--
--  Columns:
--      mutation_id: a surrogate primary. This column is referenced
--          by the relations holding the historical values of the
--          parent table.
--      principal_id: a reference to the parent table.
--      transaction_time: specifies the period during which the
--          database considered the changeset as a fact.
--      mutation_client: a reference to the {{ nspname }}.clients
--          table specifying the client through which the mutation
--          was issued.
--      mutation_principal: a reference to the {{ nspname }}.{{ relname }}
--          table specifying the principal that issued the mutation.
--
-----------------------------------------------------------------------
{% if with_drop %}
DROP TABLE IF EXISTS {{ schema_state }}.{{ relname }}_mutations CASCADE;
{% endif %}
CREATE TABLE IF NOT EXISTS {{ schema_state }}.{{ relname }}_mutations(
    mutation_id int8 NOT NULL DEFAULT nextval('{{ schema_state }}.mutations_mutation_id_seq'::regclass),
    {% for colname, type in pk  %}
    {{ colname }} {{ type }} NOT NULL,
    {% endfor %}
    mutation_timestamp public.mutation_timestamp NOT NULL,
    mutation_client public.session_client NOT NULL,
    mutation_principal public.session_user NOT NULL,
    CONSTRAINT {{ relname }}_mutations_pk
        PRIMARY KEY ({% for colname, type in pk  %}{{ colname }},{% endfor %}mutation_timestamp),
    CONSTRAINT {{ relname }}_mutations_ak1 UNIQUE (mutation_id),
    CONSTRAINT {{ relname }}_mutations_parent_fk
        FOREIGN KEY ({% for colname, type in pk  %}{{ colname }}{% if not loop.last %},{% endif %}{% endfor %})
        REFERENCES {{ nspname }}.{{ relname }} ({% for colname, type in pk  %}{{ colname }}{% if not loop.last %},{% endif %}{% endfor %})
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT {{ relname }}_mutations_mutation_client_fk
        FOREIGN KEY (mutation_client)
        REFERENCES {{ schema_entities }}.clients (client_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT {{ relname }}_mutations_mutation_principal_fk
        FOREIGN KEY (mutation_principal)
        REFERENCES {{ schema_entities }}.principals (principal_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED
);


-----------------------------------------------------------------------
--  Return a boolean indicating if a mutation exists for the entity
--  in the current transaction.
--
--  Args:
        {% for colname, datatype in pk %}
--      {{ datatype }}: primary key column.
        {%endfor %}
--
--  Returns:
--      boolean
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION {{ schema_state }}.{{ relname }}_is_mutated({% for x, datatype in pk %}{{ datatype }}{% if not loop.last %}, {% endif %}
{% endfor %}
) RETURNS boolean AS
$$
SELECT EXISTS(
    SELECT 1
    FROM {{ schema_state }}.{{ relname }}_mutations R1
    WHERE
        {% for colname, type in pk %}
        R1.{{ colname }} = ${{ loop.index }} AND
        {% endfor %}
        R1.mutation_timestamp = public.get_session_mutation_timestamp()
);
$$ LANGUAGE SQL STABLE SECURITY DEFINER;


CREATE OR REPLACE FUNCTION {{ schema_state }}.{{ relname }}_is_mutated()
RETURNS TRIGGER AS
$$
BEGIN
    IF NOT {{ schema_state }}.{{ relname }}_is_mutated({{ arglist("NEW", pk) }}) THEN
        RAISE integrity_constraint_violation USING
            MESSAGE = format(
                '%s on {{ nspname }}.{{ relname }} must create a ' ||
                '{{ schema_state }}.{{ relname }}_mutations instance', TG_OP);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;



-----------------------------------------------------------------------
--  Create a {{ schema_state }}.{{ relname }}_mutations instance.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION {{ schema_state }}.{{ relname }}_create_mutation()
RETURNS TRIGGER AS
$$
BEGIN
    IF NOT {{ schema_state }}.{{ relname }}_is_mutated({{ arglist("NEW", pk) }}) THEN
        INSERT INTO {{ schema_state }}.{{ relname }}_mutations
            ({{ columnlist(pk) }})
        VALUES ({{ arglist("NEW", pk) }});
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


CREATE OR REPLACE FUNCTION {{ schema_state }}.{{ relname }}_create_mutation({{ argspec(pk) }})
RETURNS VOID AS
$$
    INSERT INTO {{ schema_state }}.{{ relname }}_mutations
        ({{ columnlist(pk) }})
    VALUES ({% for x in pk %}${{ loop.index }}{% if not loop.last %},{% endif %}{% endfor %});
$$ LANGUAGE SQL SECURITY DEFINER;


-- Always create a {{ relname }}_mutations instance after INSERT.
DROP TRIGGER IF EXISTS create_mutation_after_insert
    ON {{ nspname }}.{{ relname }};
CREATE TRIGGER create_mutation_after_insert
    AFTER INSERT ON {{ nspname }}.{{ relname }}
    FOR EACH ROW EXECUTE PROCEDURE
    {{ schema_state }}.{{ relname }}_create_mutation();

{%- endmacro %}
