BEGIN;
-- vim: syntax=sql
-----------------------------------------------------------------------
--  Fulcrum
--
--  This is the Fulcrum header file which specifies all stored
--  procedures, types, sequences and views used by the TNGEMS/Fulcrum
--  database.
--
--  Rendered 2014-12-27 18:02:07.099567+00:00 with options:
--
--      schema_common           : common
--      schema_public           : public
--      schema_entities         : entities
--      schema_state            ; state
--      with_data               : True
--      with_drop               : True
--      with_history_drop       : False
--      with_remote_data        : True
--      with_example_data       : False
--      drop_cascade            : False
--
--
--  SYNOPSIS
--
--  This file specifies the TNG Enterprise Management System master
--  database through a series of Stuctured Query Language (SQL)
--  statements.
--
--  OVERVIEW
--
--  The TNGEMS database declares multiple schemata, logically grouping
--  tables, views and stored procedures.
--
--  -   The ``common`` schema contains data the is shared
--      by all system components, such as object type declarations and
--      ISO code lists.
--
--  -   The ``entities schema holds all domain entities.
--
--  -   The ``state schema holds the state of all domain
--      entities.
--
--
--  DESIGN CONSIDERATIONS
--
--  -   All entities that are used in decision-making should store
--      their historical state and a reference to the user and client
--      whose actions produced that state.
--
-----------------------------------------------------------------------
DROP SCHEMA IF EXISTS common CASCADE;
DROP SCHEMA IF EXISTS entities CASCADE;
DROP SCHEMA IF EXISTS state CASCADE;
DROP SCHEMA IF EXISTS system CASCADE;



-- Master schema containing application data
CREATE SCHEMA IF NOT EXISTS common;
CREATE SCHEMA IF NOT EXISTS entities;
CREATE SCHEMA IF NOT EXISTS state;

--  This is the main sequences for all domain objects that are identified
--  by a surrogate primary key.
DO
$$
BEGIN
    PERFORM 1
    FROM pg_class R1
    JOIN pg_namespace R2 ON
        R1.relnamespace = R2.oid
    WHERE
        R1.relname = 'tngems_object_id_seq' AND
        R2.nspname = 'public' AND
        R1.relkind = 'S';
    IF NOT FOUND THEN
        CREATE SEQUENCE public.tngems_object_id_seq;
    END IF;
END
$$ LANGUAGE PLPGSQL;


-- This sequence is used by all mutations.
DO
$$
BEGIN
    PERFORM 1
    FROM pg_class R1
    JOIN pg_namespace R2 ON
        R1.relnamespace = R2.oid
    WHERE
        R1.relname = 'mutations_mutation_id_seq' AND
        R2.nspname = 'state' AND
        R1.relkind = 'S';
    IF NOT FOUND THEN
        CREATE SEQUENCE state.mutations_mutation_id_seq;
    END IF;
END
$$ LANGUAGE PLPGSQL;

--  These are the extensions used by the TNGEMS/Fulcrum database. In future
--  releases a mechanism must be defined to include these extensions only
--  if they are actually needed.
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE EXTENSION IF NOT EXISTS lo;
CREATE EXTENSION IF NOT EXISTS plpython3u;
CREATE EXTENSION IF NOT EXISTS pgcrypto;


-- Set the PYTHONPATH for all subsequent commands using PL/Python so that
-- it can import libtng.
DO
$$
    import sys
    sys.path.append("/usr/lib/tngems/fulcrum/lib/python3.4/site-packages/libtng-0.5.9-py3.4.egg")

    # Import libtng and just let it raise a fatal exception if we couldnt
    # import it (the transaction will rollback).
    import libtng

    plpy.notice("libtng succesfully imported")
$$
LANGUAGE PLPYTHON3U;

-----------------------------------------------------------------------
--  Returns a timestamp with time zone indicating the state
--  timestamp of the current session.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.get_session_state_timestamp()
RETURNS timestamp with time zone AS
$$
DECLARE
    x timestamp with time zone;
BEGIN
    SELECT session_timestamp INTO x
    FROM tngems_session_state_timestamp
    LIMIT 1;
    RETURN x;
EXCEPTION
    WHEN undefined_table THEN RETURN CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;


CREATE OR REPLACE FUNCTION public.set_session_state_timestamp(
    timestamp with time zone)
RETURNS VOID AS
$$
BEGIN
    DROP TABLE IF EXISTS tngems_session_state_timestamp;
    IF $1 IS NOT NULL THEN
        CREATE TEMPORARY TABLE tngems_session_state_timestamp (
            session_timestamp timestamp with time zone PRIMARY KEY
        );
        INSERT INTO tngems_session_state_timestamp VALUES ($1);
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
-----------------------------------------------------------------------
--  Returns a timestamp with time zone indicating the mutation
--  timestamp of the current session.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.get_session_mutation_timestamp()
RETURNS timestamp with time zone AS
$$
DECLARE
    x timestamp with time zone;
BEGIN
    SELECT session_timestamp INTO x
    FROM tngems_session_mutation_timestamp
    LIMIT 1;
    RETURN x;
EXCEPTION
    WHEN undefined_table THEN RETURN CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;


CREATE OR REPLACE FUNCTION public.set_session_mutation_timestamp(
    timestamp with time zone)
RETURNS VOID AS
$$
BEGIN
    DROP TABLE IF EXISTS tngems_session_mutation_timestamp;
    IF $1 IS NOT NULL THEN
        CREATE TEMPORARY TABLE tngems_session_mutation_timestamp (
            session_timestamp timestamp with time zone PRIMARY KEY
        );
        INSERT INTO tngems_session_mutation_timestamp VALUES ($1);
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


-----------------------------------------------------------------------
--  Returns the ID of the client that is currently connected.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.get_session_client()
RETURNS int AS
$$
DECLARE
    pk int;
BEGIN
    SELECT client_id INTO pk
    FROM tngems_session_client_id;
    RETURN pk;
EXCEPTION
    WHEN undefined_table THEN RETURN NULL;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;


CREATE OR REPLACE FUNCTION public.set_session_client(int)
RETURNS VOID AS
$$
BEGIN
    DROP TABLE IF EXISTS tngems_session_client_id;
    IF $1 IS NOT NULL THEN
        CREATE TEMPORARY TABLE tngems_session_client_id (
            client_id int PRIMARY KEY
        );
        INSERT INTO tngems_session_client_id VALUES ($1);
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


CREATE OR REPLACE FUNCTION public.set_session_client(varchar)
RETURNS VOID AS
$$
BEGIN
    DROP TABLE IF EXISTS tngems_session_client_id;
    IF $1 IS NOT NULL THEN
        CREATE TEMPORARY TABLE tngems_session_client_id (
            client_id int PRIMARY KEY
        );
        INSERT INTO tngems_session_client_id
        SELECT R1.client_id
        FROM entities.clients R1
        WHERE R1.identifier = $1;
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;



-----------------------------------------------------------------------
--  Returns the ID of the user that is currently connected.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.get_session_user()
RETURNS int AS
$$
DECLARE
    pk int;
BEGIN
    SELECT user_id INTO pk
    FROM tngems_session_user_id;
    RETURN pk;
EXCEPTION
    WHEN undefined_table THEN RETURN NULL;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;


CREATE OR REPLACE FUNCTION public.set_session_user(int)
RETURNS VOID AS
$$
BEGIN
    DROP TABLE IF EXISTS tngems_session_user_id;
    IF $1 IS NOT NULL THEN
        CREATE TEMPORARY TABLE tngems_session_user_id (
            user_id int PRIMARY KEY
        );
        INSERT INTO tngems_session_user_id VALUES ($1);
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


CREATE OR REPLACE FUNCTION public.set_session_user(varchar)
RETURNS VOID AS
$$
BEGIN
    DROP TABLE IF EXISTS tngems_session_user_id;
    IF $1 IS NOT NULL THEN
        CREATE TEMPORARY TABLE tngems_session_user_id (
            user_id int PRIMARY KEY
        );
        INSERT INTO tngems_session_user_id
        SELECT R1.user_id
        FROM state.principals_username R1
        WHERE R1.username = $1;
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


-----------------------------------------------------------------------
--  Set the user/client authorization for the current transaction.
--
--  Args:
--      int: the user id.
--      int: the client_id.
--
--  Returns:
--      void
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.set_session_authorization(int, int)
RETURNS VOID AS
$$
BEGIN
    PERFORM public.set_session_user($1);
    PERFORM public.set_session_client($2);
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


-----------------------------------------------------------------------
--  Set the user/client authorization for the current transaction.
--
--  Args:
--      varchar: the user id.
--      varchar: the client_id.
--
--  Returns:
--      void
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.set_session_authorization(varchar, varchar)
RETURNS VOID AS
$$
BEGIN
    PERFORM public.set_session_user($1);
    PERFORM public.set_session_client($2);
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


-----------------------------------------------------------------------
--  Set the user/client authorization for the current transaction.
--
--  Args:
--      varchar: the user/client formatted as 'user:client'
--
--  Returns:
--      void
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.set_session_authorization(varchar)
RETURNS VOID AS
$$
DECLARE
    x varchar[];
BEGIN
    x := string_to_array($1, ':');
    PERFORM public.set_session_user(x[1]);
    PERFORM public.set_session_client(x[2]);
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;



-----------------------------------------------------------------------
--  Set automatic history for current session.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.get_auto_history()
RETURNS boolean AS
$$
DECLARE
    pk boolean;
BEGIN
    SELECT is_enabled INTO pk
    FROM tngems_auto_history_enabled;
    RETURN pk;
EXCEPTION
    WHEN undefined_table THEN RETURN FALSE;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;


CREATE OR REPLACE FUNCTION public.set_auto_history(boolean)
RETURNS VOID AS
$$
BEGIN
    DROP TABLE IF EXISTS tngems_auto_history_enabled;
    CREATE TEMPORARY TABLE tngems_auto_history_enabled (
        is_enabled boolean PRIMARY KEY
    );
    INSERT INTO tngems_auto_history_enabled VALUES ($1);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;




-- Constraint enforcing functions; these procedures are use to enforce
-- contraints, usually at the table level. We have chosen not to implement
-- these as DOMAIN types, because it would be impossible to initialize them
-- with NULL attributes.

-----------------------------------------------------------------------
--  Returns a boolean indicating if the specified value is legal for
--  use as an object transaction time.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.is_valid_transaction_time(tstzrange)
RETURNS boolean AS
$$
    SELECT isfinite(lower($1)) AND lower($1) IS NOT NULL
        AND upper($1) IS NOT NULL;
$$ LANGUAGE SQL SECURITY DEFINER IMMUTABLE RETURNS NULL ON NULL INPUT;


-----------------------------------------------------------------------
--  Validate an IPv4 address.
--
--  Args:
--      varchar: an IPv4 address.
--
--  Returns:
--      boolean
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.is_valid_ipv4(varchar)
RETURNS boolean AS
$$
    SELECT NOT EXISTS(
        SELECT x::int
        FROM unnest(string_to_array($1, '.')) x
        WHERE
            NOT int4range(0, 255, '[]') @> x::int
    );
$$ LANGUAGE SQL SECURITY DEFINER IMMUTABLE;


-----------------------------------------------------------------------
--  Assert that a hostname is a valid hostname.
--
--  Args:
--      varchar: the hostname.
--
--  Returns:
--      boolean
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.is_valid_hostname(varchar)
RETURNS boolean AS
$$
    SELECT $1 ~ '^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$';
$$ LANGUAGE SQL SECURITY DEFINER IMMUTABLE RETURNS NULL ON NULL INPUT;


-----------------------------------------------------------------------
--  Return a boolean indicating if the specified IP-address
--  identifies a single host.
--
--  Args:
--      inet: the IPv4 or IPv6 address.
--
--  Returns:
--      boolean
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.is_single_host(inet)
RETURNS boolean AS
$$
    SELECT (
        CASE
            WHEN family($1) = 6 THEN masklen($1) = 128
            WHEN family($1) = 4 THEN masklen($1) = 32
            ELSE FALSE
        END
    );
$$ LANGUAGE SQL SECURITY DEFINER IMMUTABLE RETURNS NULL ON NULL INPUT;


-----------------------------------------------------------------------
--  Assert that a given IP address is a private network.
--
--  Args:
--      inet: the IP address.
--
--  Returns:
--      boolean
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.is_private_network(inet)
RETURNS boolean AS
$$
    SELECT
        ('10.0.0.0/8'::inet >>= $1) OR
        ('172.16.0.0/12'::inet >>= $1) OR
        ('192.168.0.0/16'::inet >>= $1);
$$ LANGUAGE SQL SECURITY DEFINER IMMUTABLE RETURNS NULL ON NULL INPUT;


------------------------------------------------------------------------
--  Return a boolean indicating if a certain domain exists.
--
--  Args:
--      varchar: the schema name of the domain.
--      varchar: the name of the domain.
--
--  Returns:
--      boolean
--
------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.domain_exists(varchar, varchar)
RETURNS boolean AS
$$
    SELECT EXISTS(
        SELECT 1
        FROM pg_catalog.pg_type
        JOIN pg_catalog.pg_namespace ON
            pg_namespace.oid = pg_type.typnamespace
        WHERE
            typtype = 'd' AND
            lower(nspname) = lower($1) AND
            lower(typname) = lower($2)
    );
$$ LANGUAGE SQL;


-----------------------------------------------------------------------
--  Domain  types
--
-----------------------------------------------------------------------
DO $$
BEGIN
DROP DOMAIN IF EXISTS public.transaction_time CASCADE;
DROP DOMAIN IF EXISTS public.mutation_timestamp CASCADE;

IF NOT public.domain_exists('public', 'transaction_time') THEN
    CREATE DOMAIN public.transaction_time AS tstzrange
        DEFAULT tstzrange(public.get_session_mutation_timestamp(), 
            'infinity', '[)')
        CONSTRAINT transaction_time_bounds_chk CHECK (
            lower(VALUE) IS NOT NULL AND
            isfinite(lower(VALUE)) AND
            upper(VALUE) IS NOT NULL
        );
END IF;


IF NOT public.domain_exists('public', 'mutation_timestamp') THEN
    CREATE DOMAIN public.mutation_timestamp AS timestamp with time zone
        DEFAULT public.get_session_mutation_timestamp();
END IF;


IF NOT public.domain_exists('public', 'session_user') THEN
    CREATE DOMAIN public.session_user AS int
        DEFAULT public.get_session_user();
END IF;


IF NOT public.domain_exists('public', 'session_client') THEN
    CREATE DOMAIN public.session_client AS int
        DEFAULT public.get_session_client();
END IF;


IF NOT public.domain_exists('public', 'identifier') THEN
    CREATE DOMAIN public.identifier AS varchar
        CONSTRAINT identifier_valid_pattern
        CHECK (VALUE != '');
END IF;


IF NOT public.domain_exists('public', 'string') THEN
    CREATE DOMAIN public.string AS varchar
        CONSTRAINT string_valid_pattern
        CHECK (VALUE != '');
END IF;
ALTER DOMAIN public.string DROP NOT NULL;


IF NOT public.domain_exists('public', 'username') THEN
    CREATE DOMAIN public.username AS varchar
        CONSTRAINT username_valid_pattern
        CHECK (VALUE != '');
END IF;


IF NOT public.domain_exists('public', 'rsapublic') THEN
    CREATE DOMAIN public.rsapublic AS varchar
        CONSTRAINT rsa_public_valid_pattern
        CHECK (VALUE ~ 'ssh-rsa AAAA[0-9A-Za-z+/]+[=]{0,3}');
END IF;

IF NOT public.domain_exists('public', 'ipv4') THEN
    CREATE DOMAIN public.ipv4 AS varchar
        CONSTRAINT ipv4_valid
        CHECK (public.is_valid_ipv4(VALUE));
END IF;


IF NOT public.domain_exists('public', 'hostname') THEN
    CREATE DOMAIN public.hostname AS varchar
        CONSTRAINT hostname_valid
        CHECK (public.is_valid_hostname(VALUE));
END IF;


IF NOT public.domain_exists('public', 'ipaddress') THEN
    CREATE DOMAIN public.ipaddress AS inet
        CONSTRAINT ipaddress_valid
        CHECK (public.is_single_host(VALUE));
END IF;


IF NOT public.domain_exists('public', 'filepath') THEN
    CREATE DOMAIN public.filepath AS varchar
        CONSTRAINT filepath_valid
        CHECK (VALUE ~ '^((/[\d\w\_\-\.]+)+|/)$'); -- TODO: probably does not work with Unicode
END IF;


IF NOT public.domain_exists('public', 'mimetype') THEN
    CREATE DOMAIN public.mimetype AS varchar
        CONSTRAINT mimetype_pattern
        CHECK (VALUE ~ '^(application|audio|example|image|message|model|multipart|text|video)/.*$');
END IF;


IF NOT public.domain_exists('public', 'surah') THEN
    CREATE DOMAIN public.surah AS smallint
        CONSTRAINT surah_number_valid
        CHECK (int4range(1, 114, '[]') @> VALUE::int);
END IF;



IF NOT public.domain_exists('public', 'slug') THEN
    CREATE DOMAIN public.slug AS varchar
        CONSTRAINT slug_valid
        CHECK (VALUE ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$');
END IF;


IF NOT public.domain_exists('public', 'phonenumber') THEN
    CREATE DOMAIN public.phonenumber AS varchar
        CONSTRAINT phonenumber_valid
        CHECK (VALUE ~ '^\+[0-9]{8,}$');
END IF;



-----------------------------------------------------------------------
--  Specifies a gender type domain. Though the subject is complicated due
--  to identity/biological complexities, the domain tries to be as
--  comprehensive as possible. The gender domain is to be used for a
--  persons phenotype in common applications; e.g. medical applications
--  should define their own domain for specifying a persons genotype.
--
--  Values are:
--      M: Male
--      F: Female
--      N: Neither
--      B: Both
--      D: Decline to state
--      C: It's complicated
--      X: Unknown.
--
--  See also http://www.sarahdopp.com/blog/2010/designing-a-better-drop-down-menu-for-gender/
--
-----------------------------------------------------------------------
IF NOT public.domain_exists('public', 'gender') THEN
    CREATE DOMAIN public.gender AS varchar(1)
        CHECK (VALUE IN ('M','F','N','B','D','C','X'));
END IF;


END;
$$ LANGUAGE plpgsql;


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  UNIT OF MEASUREMENT DATA DEFINITION LANGUAGE (DDL)
--
-----------------------------------------------------------------------
DROP TABLE IF EXISTS
    common.unitsofmeasure CASCADE;
DROP TABLE IF EXISTS
    common.unitofmeasureconversions CASCADE;


-----------------------------------------------------------------------
--  UNIT OF MEASUREMENT
--
--  Columns:
--      quantity: specifies the quantity of the unit of measurement.
--          Only units of the same quantity can be compared with
--          each other.
--      code: the primary key.
--      display_name: a token display name for the unit of measurement.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS common.unitsofmeasure(
    quantity varchar NOT NULL,
    codename public.slug NOT NULL,
    display_name public.string NOT NULL,
    CONSTRAINT unitsofmeasure_pk
        PRIMARY KEY (codename)
);


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  UNIT OF MEASUREMENT INITIAL DATA
--
-----------------------------------------------------------------------

--  The SI system has seven base quantities:
--
--  Length (l)
--  Mass (m)
--  Time (t)
--  Electric current
--  Temperature
--  Amount of substance
--  Luminous intensity
--  
WITH initial_data(quantity, codename, display_name) AS (
    VALUES
        ('l', 'meter', 'UOM_SI_METER'),
        ('m', 'gram', 'UOM_SI_GRAM'),
        ('m', 'kilogram', 'UOM_SI_KILOGRAM')
)
INSERT INTO common.unitsofmeasure
    (quantity, codename, display_name)
SELECT quantity, codename, display_name
FROM initial_data
WHERE codename NOT IN (
    SELECT codename
    FROM common.unitsofmeasure
);


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  VALUE ADDED TAX DATA-DEFINITION LANGUAGE
--
--  This file specified the Data Definition Language of a datamodel for
--  storing Value Added Tax rates and rules.
--
-----------------------------------------------------------------------
DROP TABLE IF EXISTS
    common.vatratetypes CASCADE;
DROP TABLE IF EXISTS
    common.vatrates CASCADE;

-----------------------------------------------------------------------
--  VAT RATE TYPE
--
--  Defines a VAT rate type for a specific country.
--
--  Columns:
--      imposing_country: the country that specified the rate.
--      name: a unique name for rate/country.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS common.vatratetypes(
    imposing_country varchar(2) NOT NULL,
    name varchar NOT NULL,
    CONSTRAINT vatratetypes_pk
        PRIMARY KEY (imposing_country, name)
);


-----------------------------------------------------------------------
--  VAT RATE
--
--  Specifies  a VAT rate for a certain period.
--
--  Columns:
--      imposing_country: an ISO 3166 country code specifying the 
--          first-order administrative division that imposes the
--          VAT rate.
--      name: an identifier for the VAT rate.
--      during: specifies the period during which the VAT rate was
--          imposed. Defaults to ('-infinity','infinity').
--      rate: the VAT rate as a fraction of 1.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS common.vatrates(
    imposing_country varchar(2) NOT NULL,
    name varchar NOT NULL,
    during daterange NOT NULL
        DEFAULT daterange('-infinity','infinity'),
    rate numeric NOT NULL,
    CONSTRAINT vatrates_pk
        PRIMARY KEY (imposing_country, name, during),
    CONSTRAINT vatrates_during_excl
        EXCLUDE USING GIST (imposing_country WITH =, name WITH =,
            during WITH &&),
    CONSTRAINT vatrates_during_adj
        EXCLUDE USING GIST (imposing_country WITH =, name WITH =,
            rate WITH =, during WITH -|-),
    CONSTRAINT vatrates_vatratetypes_fk1
        FOREIGN KEY (imposing_country, name)
        REFERENCES common.vatratetypes (imposing_country, name)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE
);


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  VALUE ADDED TAX MODULE STORED PROCEDURES
--
-----------------------------------------------------------------------


-----------------------------------------------------------------------
--  Back-calculates the Value Added Tax (VAT) from a specified amount.
--  Return a `decimal(19, 6)` indicating the VAT amount.
--
--  Args:
--      varchar(2): An ISO 3166-1 Alpha 2 country code identiying the
--          country whose VAT policy is to be applied.
--      varchar: identifies the VAT rate to apply.
--      decimal(19,6): specifies the monetary amount.
--
--  Returns:
--      decimal(19,6)
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION common.calculate_vat_amount(
    varchar(2), varchar, decimal(19,6))
RETURNS decimal(19,6) AS
$$
BEGIN
    -- stub
    RETURN '0.0'::decimal;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  VALUE ADDED TAX SCHEMA INITIAL DATA
--
-----------------------------------------------------------------------

-- common.vatratetypes initial data
WITH initial_data(imposing_country, name) AS (
    VALUES
        ('DE', 'low'),
        ('DE', 'high'),
        ('NL', 'low'),
        ('NL', 'standard')
)
INSERT INTO common.vatratetypes (imposing_country, name)
SELECT T.imposing_country, T.name
FROM initial_data T
EXCEPT
SELECT R.imposing_country, R.name
FROM common.vatratetypes R;


-- common.vatrates initial data
WITH initial_data(imposing_country, name, start_date, end_date, rate) AS (
    VALUES
        ('DE', 'low', '1968-01-01'::date, '1968-01-06'::date, '0.05'::numeric),
        ('DE', 'low', '1968-06-01'::date, '1978-01-01'::date, '0.055'::numeric),
        ('DE', 'low', '1978-01-01'::date, '1979-06-01'::date, '0.06'::numeric),
        ('DE', 'low', '1979-06-01'::date, '1983-06-01'::date, '0.065'::numeric),
        ('DE', 'low', '1983-06-01'::date, 'infinity'::date, '0.07'::numeric),
        ('DE', 'high', '1968-01-01'::date, '1968-01-06'::date, '0.10'::numeric),
        ('DE', 'high', '1968-06-01'::date, '1978-01-01'::date, '0.11'::numeric),
        ('DE', 'high', '1978-01-01'::date, '1979-06-01'::date, '0.12'::numeric),
        ('DE', 'high', '1979-06-01'::date, '1983-06-01'::date, '0.13'::numeric),
        ('DE', 'high', '1983-06-01'::date, '1993-01-01'::date, '0.14'::numeric),
        ('DE', 'high', '1993-01-01'::date, '1998-04-01'::date, '0.15'::numeric),
        ('DE', 'high', '1998-04-01'::date, '2007-01-01'::date, '0.16'::numeric),
        ('DE', 'high', '2007-01-01'::date, 'infinity'::date, '0.19'::numeric),
        ('NL', 'low', '1969-01-01'::date, '1984-01-01'::date, '0.04'::numeric),
        ('NL', 'low', '1984-01-01'::date, '1986-10-01'::date, '0.05'::numeric),
        ('NL', 'low', '1986-10-01'::date, 'infinity'::date, '0.06'::numeric),
        ('NL', 'standard', '1969-01-01'::date, '1971-01-01'::date, '0.12'::numeric),
        ('NL', 'standard', '1971-01-01'::date, '1973-01-01'::date, '0.14'::numeric),
        ('NL', 'standard', '1973-01-01'::date, '1976-10-01'::date, '0.16'::numeric),
        ('NL', 'standard', '1976-10-01'::date, '1984-01-01'::date, '0.18'::numeric),
        ('NL', 'standard', '1984-01-01'::date, '1986-10-01'::date, '0.19'::numeric),
        ('NL', 'standard', '1986-10-01'::date, '1989-01-01'::date, '0.20'::numeric),
        ('NL', 'standard', '1989-01-01'::date, '1992-10-01'::date, '0.185'::numeric),
        ('NL', 'standard', '1992-10-01'::date, '2001-01-01'::date, '0.175'::numeric),
        ('NL', 'standard', '2001-01-01'::date, '2012-01-01'::date, '0.19'::numeric),
        ('NL', 'standard', '2012-10-01'::date, 'infinity'::date, '0.21'::numeric)
),
upsert AS (
    UPDATE common.vatrates R SET
        during = daterange(I.start_date, I.end_date),
        rate = I.rate
    FROM initial_data I
    WHERE
        R.imposing_country = I.imposing_country AND
        R.name = I.name AND
        lower(R.during) = I.start_date
    RETURNING R.*
)
INSERT INTO common.vatrates
    (imposing_country, name, during, rate)
SELECT imposing_country, name, daterange(start_date::date, end_date::date), rate
FROM initial_data
WHERE
    (imposing_country, name, start_date) NOT IN (
        SELECT imposing_country, name, lower(during)
        FROM upsert
    )
;


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  UNIT OF MEASUREMENT DATA DEFINITION LANGUAGE (DDL)
--
-----------------------------------------------------------------------
DROP TABLE IF EXISTS
    common.unitsofmeasure CASCADE;
DROP TABLE IF EXISTS
    common.unitofmeasureconversions CASCADE;


-----------------------------------------------------------------------
--  UNIT OF MEASUREMENT
--
--  Columns:
--      quantity: specifies the quantity of the unit of measurement.
--          Only units of the same quantity can be compared with
--          each other.
--      code: the primary key.
--      display_name: a token display name for the unit of measurement.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS common.unitsofmeasure(
    quantity varchar NOT NULL,
    codename public.slug NOT NULL,
    display_name public.string NOT NULL,
    CONSTRAINT unitsofmeasure_pk
        PRIMARY KEY (codename)
);


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  UNIT OF MEASUREMENT INITIAL DATA
--
-----------------------------------------------------------------------

--  The SI system has seven base quantities:
--
--  Length (l)
--  Mass (m)
--  Time (t)
--  Electric current
--  Temperature
--  Amount of substance
--  Luminous intensity
--  
WITH initial_data(quantity, codename, display_name) AS (
    VALUES
        ('l', 'meter', 'UOM_SI_METER'),
        ('m', 'gram', 'UOM_SI_GRAM'),
        ('m', 'kilogram', 'UOM_SI_KILOGRAM')
)
INSERT INTO common.unitsofmeasure
    (quantity, codename, display_name)
SELECT quantity, codename, display_name
FROM initial_data
WHERE codename NOT IN (
    SELECT codename
    FROM common.unitsofmeasure
);


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  TOP-LEVEL DOMAIN NAME DDL, VIEWS, PROCEDURES AND TRIGGERS
--
-----------------------------------------------------------------------
DROP TABLE IF EXISTS
    common.topleveldomains CASCADE;


-----------------------------------------------------------------------
--  TOP LEVEL DOMAIN NAME
--
--  Describes a top-level domain (TLD), one of the domains at the
--  highest level in the hierarchical Domain Name System of the Internet.
--  The top-level domain names are installed in the root zone of the
--  name space.
--
--  Columns:
--      country_code: an ISO 3166-2 code specifying the country.
--      tld: the TLD.
--
--  Notes:
--      -   `tld` may not begin with a dot (.).
--      -   `tld` may not end with a dot (.).
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS common.topleveldomains(
    tld varchar NOT NULL,
    CONSTRAINT topleveldomains_pk
        PRIMARY KEY (tld),
    CONSTRAINT topleveldomains_tld_chk1
        CHECK (tld != ''),
    CONSTRAINT topleveldomains_tld_chk2
        CHECK (NOT tld ~ '^\..*$'),
    CONSTRAINT topleveldomains_tld_chk3
        CHECK (NOT tld ~ '^.*\.$')
);


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  TOP-LEVEL DOMAIN NAME STORED PROCEDURES
--
-----------------------------------------------------------------------


-----------------------------------------------------------------------
--  Return a set of valid top-level domain names.
--
--  Returns:
--      setof varchar
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.get_valid_tlds()
RETURNS TABLE (
    tld varchar
) AS
$$
try:
    import libtng.dns

    return libtng.dns.get_valid_tlds()
except ImportError:
     plpy.fatal("Unable to import libtng. Is it on sys.path?")
$$ LANGUAGE PLPYTHON3U STABLE SECURITY DEFINER;


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  TOP-LEVEL DOMAIN NAME INITIAL DATA
--
-----------------------------------------------------------------------
INSERT INTO common.topleveldomains (tld)
SELECT R1.tld
FROM public.get_valid_tlds() R1
WHERE R1.tld NOT IN (
    SELECT tld
    FROM common.topleveldomains
);



-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  SOUSOU IDENTITY MANAGEMENT SYSTEM DATA DEFINITION LANGUAGE (DDL)
--
--  This file contains the Data Definition Language (DDL) statements to
--  create the Sousou IMS schema.
--
--  The Sousou IMS specifies the following objects:
--
--  Principal:
--  Client:
--
-----------------------------------------------------------------------
DROP TABLE IF EXISTS entities.principals CASCADE;
DROP TABLE IF EXISTS entities.clients CASCADE;


-----------------------------------------------------------------------
--  CLIENT
--
--  Represents a access point to the TNG Enterprise Management System.
--
--  Columns:
--      client_id: a surrogate primary key.
--      codename: an mnemmonic identifier.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.clients(
    client_id int8 NOT NULL
        DEFAULT nextval('tngems_object_id_seq'),
    codename varchar NOT NULL,
    CONSTRAINT clients_pk
        PRIMARY KEY (client_id),
    CONSTRAINT clients_ak1
        UNIQUE (codename)
);


-----------------------------------------------------------------------
--  PRINCIPAL
--
--  Columns:
--      principal_id: a surrogate primary key.
--      subtype: a discriminator column identifying the subtype.
--      date_registered: indicates the date and time the account was
--          created.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.principals(
    principal_id int8 NOT NULL
        DEFAULT nextval('tngems_object_id_seq'),
    subtype varchar NOT NULL,
    date_registered timestamp with time zone NOT NULL,
    CONSTRAINT principals_pk
        PRIMARY KEY (principal_id),
    CONSTRAINT principals_subtype_valid
        CHECK (subtype IN ('user','auto'))
);


-----------------------------------------------------------------------
--  Principals Mutation
--
--  Describes a mutation on entities.principals.
--
--  Columns:
--      mutation_id: a surrogate primary. This column is referenced
--          by the relations holding the historical values of the
--          parent table.
--      principal_id: a reference to the parent table.
--      transaction_time: specifies the period during which the
--          database considered the changeset as a fact.
--      mutation_client: a reference to the entities.clients
--          table specifying the client through which the mutation
--          was issued.
--      mutation_principal: a reference to the entities.principals
--          table specifying the principal that issued the mutation.
--
-----------------------------------------------------------------------
DROP TABLE IF EXISTS state.principals_mutations CASCADE;
CREATE TABLE IF NOT EXISTS state.principals_mutations(
    mutation_id int8 NOT NULL DEFAULT nextval('state.mutations_mutation_id_seq'::regclass),
    principal_id int8 NOT NULL,
    mutation_timestamp public.mutation_timestamp NOT NULL,
    mutation_client public.session_client NOT NULL,
    mutation_principal public.session_user NOT NULL,
    CONSTRAINT principals_mutations_pk
        PRIMARY KEY (principal_id,mutation_timestamp),
    CONSTRAINT principals_mutations_ak1 UNIQUE (mutation_id),
    CONSTRAINT principals_mutations_parent_fk
        FOREIGN KEY (principal_id)
        REFERENCES entities.principals (principal_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT principals_mutations_mutation_client_fk
        FOREIGN KEY (mutation_client)
        REFERENCES entities.clients (client_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT principals_mutations_mutation_principal_fk
        FOREIGN KEY (mutation_principal)
        REFERENCES entities.principals (principal_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED
);


-----------------------------------------------------------------------
--  Return a boolean indicating if a mutation exists for the entity
--  in the current transaction.
--
--  Args:
--      int8: primary key column.
--
--  Returns:
--      boolean
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION state.principals_is_mutated(int8) RETURNS boolean AS
$$
SELECT EXISTS(
    SELECT 1
    FROM state.principals_mutations R1
    WHERE
        R1.principal_id = $1 AND
        R1.mutation_timestamp = public.get_session_mutation_timestamp()
);
$$ LANGUAGE SQL STABLE SECURITY DEFINER;


CREATE OR REPLACE FUNCTION state.principals_is_mutated()
RETURNS TRIGGER AS
$$
BEGIN
    IF NOT state.principals_is_mutated(NEW.principal_id) THEN
        RAISE integrity_constraint_violation USING
            MESSAGE = format(
                '%s on entities.principals must create a ' ||
                'state.principals_mutations instance', TG_OP);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;



-----------------------------------------------------------------------
--  Create a state.principals_mutations instance.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION state.principals_create_mutation()
RETURNS TRIGGER AS
$$
BEGIN
    IF NOT state.principals_is_mutated(NEW.principal_id) THEN
        INSERT INTO state.principals_mutations
            (principal_id)
        VALUES (NEW.principal_id);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


CREATE OR REPLACE FUNCTION state.principals_create_mutation(int8)
RETURNS VOID AS
$$
    INSERT INTO state.principals_mutations
        (principal_id)
    VALUES ($1);
$$ LANGUAGE SQL SECURITY DEFINER;


-- Always create a principals_mutations instance after INSERT.
DROP TRIGGER IF EXISTS create_mutation_after_insert
    ON entities.principals;
CREATE TRIGGER create_mutation_after_insert
    AFTER INSERT ON entities.principals
    FOR EACH ROW EXECUTE PROCEDURE
    state.principals_create_mutation();


--  States that a PRINCIPAL identified by `principal_id` had it's
--  Attribute Username set to `username` in the period 
--  `transaction_time`.
DROP TABLE IF EXISTS
    state.principals_username CASCADE;
CREATE TABLE IF NOT EXISTS state.principals_username(
    mutation_timestamp public.mutation_timestamp NOT NULL,
    principal_id int8 NOT NULL,
    transaction_time public.transaction_time NOT NULL,
    username public.string NOT NULL,
    CONSTRAINT principals_username_pk
        PRIMARY KEY (mutation_timestamp, principal_id),
    CONSTRAINT principals_username_principals_mutations_fk1
        FOREIGN KEY (mutation_timestamp, principal_id)
        REFERENCES state.principals_mutations (
            mutation_timestamp, principal_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT principals_username_mutation_timestamp
        CHECK (mutation_timestamp = lower(transaction_time)),
    CONSTRAINT principals_username_transaction_time_excl
        EXCLUDE USING GIST (principal_id WITH =, transaction_time WITH &&),
    CONSTRAINT principals_username_transaction_time_adj
        EXCLUDE USING GIST (
            principal_id WITH =,
            (username) WITH =,
            transaction_time WITH -|-
    )
);


-- Update the existing transaction time before inserting.
CREATE OR REPLACE FUNCTION state.principals_username__mutate()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE state.principals_username SET
        transaction_time = tstzrange(lower(transaction_time),
            public.get_session_mutation_timestamp())
    WHERE
        principal_id = NEW.principal_id AND
        transaction_time @> public.get_session_mutation_timestamp();
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


DROP TRIGGER IF EXISTS end_transaction_time
    ON state.principals_username CASCADE;
CREATE TRIGGER end_transaction_time 
    BEFORE INSERT ON state.principals_username
    FOR EACH ROW EXECUTE PROCEDURE 
    state.principals_username__mutate();


--  States that a PRINCIPAL identified by `principal_id` had it's
--  Attribute Email Address set to `email_address` in the period 
--  `transaction_time`.
DROP TABLE IF EXISTS
    state.principals_email_address CASCADE;
CREATE TABLE IF NOT EXISTS state.principals_email_address(
    mutation_timestamp public.mutation_timestamp NOT NULL,
    principal_id int8 NOT NULL,
    transaction_time public.transaction_time NOT NULL,
    email_address public.string NOT NULL,
    CONSTRAINT principals_email_address_pk
        PRIMARY KEY (mutation_timestamp, principal_id),
    CONSTRAINT principals_email_address_principals_mutations_fk1
        FOREIGN KEY (mutation_timestamp, principal_id)
        REFERENCES state.principals_mutations (
            mutation_timestamp, principal_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT principals_email_address_mutation_timestamp
        CHECK (mutation_timestamp = lower(transaction_time)),
    CONSTRAINT principals_email_address_transaction_time_excl
        EXCLUDE USING GIST (principal_id WITH =, transaction_time WITH &&),
    CONSTRAINT principals_email_address_transaction_time_adj
        EXCLUDE USING GIST (
            principal_id WITH =,
            (email_address) WITH =,
            transaction_time WITH -|-
    )
);


-- Update the existing transaction time before inserting.
CREATE OR REPLACE FUNCTION state.principals_email_address__mutate()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE state.principals_email_address SET
        transaction_time = tstzrange(lower(transaction_time),
            public.get_session_mutation_timestamp())
    WHERE
        principal_id = NEW.principal_id AND
        transaction_time @> public.get_session_mutation_timestamp();
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


DROP TRIGGER IF EXISTS end_transaction_time
    ON state.principals_email_address CASCADE;
CREATE TRIGGER end_transaction_time 
    BEFORE INSERT ON state.principals_email_address
    FOR EACH ROW EXECUTE PROCEDURE 
    state.principals_email_address__mutate();


--  States that a PRINCIPAL identified by `principal_id` had it's
--  Attribute Passphrase set to `passphrase` in the period 
--  `transaction_time`.
DROP TABLE IF EXISTS
    state.principals_passphrase CASCADE;
CREATE TABLE IF NOT EXISTS state.principals_passphrase(
    mutation_timestamp public.mutation_timestamp NOT NULL,
    principal_id int8 NOT NULL,
    transaction_time public.transaction_time NOT NULL,
    passphrase public.string NOT NULL,
    CONSTRAINT principals_passphrase_pk
        PRIMARY KEY (mutation_timestamp, principal_id),
    CONSTRAINT principals_passphrase_principals_mutations_fk1
        FOREIGN KEY (mutation_timestamp, principal_id)
        REFERENCES state.principals_mutations (
            mutation_timestamp, principal_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT principals_passphrase_mutation_timestamp
        CHECK (mutation_timestamp = lower(transaction_time)),
    CONSTRAINT principals_passphrase_transaction_time_excl
        EXCLUDE USING GIST (principal_id WITH =, transaction_time WITH &&),
    CONSTRAINT principals_passphrase_transaction_time_adj
        EXCLUDE USING GIST (
            principal_id WITH =,
            (passphrase) WITH =,
            transaction_time WITH -|-
    )
);


-- Update the existing transaction time before inserting.
CREATE OR REPLACE FUNCTION state.principals_passphrase__mutate()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE state.principals_passphrase SET
        transaction_time = tstzrange(lower(transaction_time),
            public.get_session_mutation_timestamp())
    WHERE
        principal_id = NEW.principal_id AND
        transaction_time @> public.get_session_mutation_timestamp();
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


DROP TRIGGER IF EXISTS end_transaction_time
    ON state.principals_passphrase CASCADE;
CREATE TRIGGER end_transaction_time 
    BEFORE INSERT ON state.principals_passphrase
    FOR EACH ROW EXECUTE PROCEDURE 
    state.principals_passphrase__mutate();



-- The `is_active` and `is_deleted` should probably be timestamp ranges,
-- but this would require additional constraints (no overlapping ranges
-- for both the attribute and the transaction time).
--  States that a PRINCIPAL identified by `principal_id` had it's
--  Attribute Is active set to `is_active` in the period 
--  `transaction_time`.
DROP TABLE IF EXISTS
    state.principals_is_active CASCADE;
CREATE TABLE IF NOT EXISTS state.principals_is_active(
    mutation_timestamp public.mutation_timestamp NOT NULL,
    principal_id int8 NOT NULL,
    transaction_time public.transaction_time NOT NULL,
    is_active boolean NOT NULL,
    CONSTRAINT principals_is_active_pk
        PRIMARY KEY (mutation_timestamp, principal_id),
    CONSTRAINT principals_is_active_principals_mutations_fk1
        FOREIGN KEY (mutation_timestamp, principal_id)
        REFERENCES state.principals_mutations (
            mutation_timestamp, principal_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT principals_is_active_mutation_timestamp
        CHECK (mutation_timestamp = lower(transaction_time)),
    CONSTRAINT principals_is_active_transaction_time_excl
        EXCLUDE USING GIST (principal_id WITH =, transaction_time WITH &&),
    CONSTRAINT principals_is_active_transaction_time_adj
        EXCLUDE USING GIST (
            principal_id WITH =,
            (is_active::int::smallint) WITH =,
            transaction_time WITH -|-
    )
);


-- Update the existing transaction time before inserting.
CREATE OR REPLACE FUNCTION state.principals_is_active__mutate()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE state.principals_is_active SET
        transaction_time = tstzrange(lower(transaction_time),
            public.get_session_mutation_timestamp())
    WHERE
        principal_id = NEW.principal_id AND
        transaction_time @> public.get_session_mutation_timestamp();
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


DROP TRIGGER IF EXISTS end_transaction_time
    ON state.principals_is_active CASCADE;
CREATE TRIGGER end_transaction_time 
    BEFORE INSERT ON state.principals_is_active
    FOR EACH ROW EXECUTE PROCEDURE 
    state.principals_is_active__mutate();


--  States that a PRINCIPAL identified by `principal_id` had it's
--  Attribute Is deleted set to `is_deleted` in the period 
--  `transaction_time`.
DROP TABLE IF EXISTS
    state.principals_is_deleted CASCADE;
CREATE TABLE IF NOT EXISTS state.principals_is_deleted(
    mutation_timestamp public.mutation_timestamp NOT NULL,
    principal_id int8 NOT NULL,
    transaction_time public.transaction_time NOT NULL,
    is_deleted boolean NOT NULL,
    CONSTRAINT principals_is_deleted_pk
        PRIMARY KEY (mutation_timestamp, principal_id),
    CONSTRAINT principals_is_deleted_principals_mutations_fk1
        FOREIGN KEY (mutation_timestamp, principal_id)
        REFERENCES state.principals_mutations (
            mutation_timestamp, principal_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT principals_is_deleted_mutation_timestamp
        CHECK (mutation_timestamp = lower(transaction_time)),
    CONSTRAINT principals_is_deleted_transaction_time_excl
        EXCLUDE USING GIST (principal_id WITH =, transaction_time WITH &&),
    CONSTRAINT principals_is_deleted_transaction_time_adj
        EXCLUDE USING GIST (
            principal_id WITH =,
            (is_deleted::int::smallint) WITH =,
            transaction_time WITH -|-
    )
);


-- Update the existing transaction time before inserting.
CREATE OR REPLACE FUNCTION state.principals_is_deleted__mutate()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE state.principals_is_deleted SET
        transaction_time = tstzrange(lower(transaction_time),
            public.get_session_mutation_timestamp())
    WHERE
        principal_id = NEW.principal_id AND
        transaction_time @> public.get_session_mutation_timestamp();
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


DROP TRIGGER IF EXISTS end_transaction_time
    ON state.principals_is_deleted CASCADE;
CREATE TRIGGER end_transaction_time 
    BEFORE INSERT ON state.principals_is_deleted
    FOR EACH ROW EXECUTE PROCEDURE 
    state.principals_is_deleted__mutate();



-- Relation-specific constraints
ALTER TABLE state.principals_username
    DROP CONSTRAINT IF EXISTS principals_username_excl CASCADE;
ALTER TABLE state.principals_username
    ADD CONSTRAINT principals_username_excl
    EXCLUDE USING GIST (username WITH =, transaction_time WITH &&);


ALTER TABLE state.principals_email_address
    DROP CONSTRAINT IF EXISTS principals_email_address_excl CASCADE;
ALTER TABLE state.principals_email_address
    ADD CONSTRAINT principals_email_address_excl
    EXCLUDE USING GIST (email_address WITH =, transaction_time WITH &&);



-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  SOUSOU IDENTITY MANAGEMENT SYSTEM VIRTUAL RELATIONS
--
--  This file declares the virtual relations used by the Sousou IMS.
--
-----------------------------------------------------------------------
DROP VIEW IF EXISTS public.principals CASCADE;
DROP VIEW IF EXISTS public.credentials CASCADE;
DROP VIEW IF EXISTS state.principals CASCADE;


--  The current state view for PRINCIPAL entities.
CREATE VIEW public.principals AS
    SELECT
        R1.principal_id,
        R1.subtype,
        R1.date_registered,
        R2.is_active,
        COALESCE(R4.email_address, '') AS email_address,
        COALESCE(R5.username, '') AS username
    FROM entities.principals R1
    JOIN state.principals_is_active R2 ON
        R1.principal_id = R2.principal_id AND
        R2.transaction_time @> public.get_session_state_timestamp()
    JOIN state.principals_is_deleted R3 ON
        R1.principal_id = R3.principal_id AND
        R3.transaction_time @> public.get_session_state_timestamp()
    LEFT OUTER JOIN state.principals_email_address R4 ON
        R1.principal_id = R4.principal_id AND
        R4.transaction_time @> public.get_session_state_timestamp()
    LEFT OUTER JOIN state.principals_username R5 ON
        R1.principal_id = R5.principal_id AND
        R5.transaction_time @> public.get_session_state_timestamp()
    WHERE NOT R3.is_deleted;


ALTER VIEW public.principals ALTER COLUMN is_active SET DEFAULT FALSE;


-----------------------------------------------------------------------
--  Mutation procedure for public.principals
--
--  A mutation procedure should make the following state changes:
--
--  -   Insert into state.principals_mutations
--      (if applicable).
--  -   Insert or update the underlying base relations.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.principals__mutate(
    TG_OP varchar,
    TG_ARGV varchar[],
    TG_NARGS int,
    TG_TABLE_SCHEMA name,
    TG_TABLE_NAME name,
    OLD public.principals,
    NEW public.principals
)
RETURNS public.principals AS
$$
DECLARE
    obj public.principals;
BEGIN
    -- Bail out early if the record was not changed.
    IF TG_OP = 'UPDATE' AND NEW IS NOT DISTINCT FROM OLD THEN
        RETURN NEW;
    END IF;
    obj := CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
    IF TG_OP = 'INSERT' THEN
        IF obj.principal_id IS NULL THEN
            INSERT INTO entities.principals
                (principal_id, subtype, date_registered)
            VALUES (DEFAULT, obj.subtype, obj.date_registered)
            RETURNING principal_id INTO obj.principal_id;
        ELSE
            INSERT INTO entities.principals
                (principal_id, subtype, date_registered)
            VALUES (obj.principal_id, obj.subtype, obj.date_registered)
            RETURNING principal_id INTO obj.principal_id;
        END IF;
    END IF;
    IF NOT state.principals_is_mutated(obj.principal_id) THEN
        PERFORM state.principals_create_mutation(obj.principal_id);
    END IF;
    CASE
        WHEN TG_OP IN ('INSERT','UPDATE') THEN
            IF TG_OP = 'INSERT' THEN
                -- Mark the object as not deleted here, since inserting AND deleting
                -- will never happen.
                INSERT INTO state.principals_is_deleted
                    (principal_id, is_deleted)
                VALUES (obj.principal_id, FALSE);
            END IF;

            -- Stateful attributes are persisted below.
            IF obj.is_active IS DISTINCT FROM OLD.is_active
            OR TG_OP = 'INSERT' THEN
                INSERT INTO state.principals_is_active
                    (principal_id, is_active)
                VALUES
                    (obj.principal_id, obj.is_active);
            END IF;

            IF COALESCE(obj.email_address, '') != '' 
            AND (
                obj.email_address IS DISTINCT FROM OLD.email_address
                OR TG_OP = 'INSERT'
            ) THEN
                INSERT INTO state.principals_email_address
                    (principal_id, email_address)
                VALUES (obj.principal_id, obj.email_address);
            END IF;

            IF COALESCE(obj.username, '') != ''
            AND (
                obj.username IS DISTINCT FROM OLD.username
                OR TG_OP = 'INSERT'
            ) THEN
                INSERT INTO state.principals_username
                    (principal_id, username)
                VALUES (obj.principal_id, obj.username);
            END IF;
        WHEN TG_OP = 'DELETE' THEN
            INSERT INTO state.principals_is_deleted
                (principal_id, is_deleted)
            VALUES (obj.principal_id, TRUE);
        ELSE
            RAISE invalid_parameter_value USING
                MESSAGE = format('Invalid TG_OP: %s', TG_OP),
                HINT = format('Use either INSERT, UPDATE, DELETE or TRUNCATE');
    END CASE;
    RETURN obj;
END;
$$ LANGUAGE PLPGSQL SECURITY INVOKER;

-----------------------------------------------------------------------
--  End mutation procedure public.principals__mutate()
-----------------------------------------------------------------------


-----------------------------------------------------------------------
--  UPDATABLE VIRTUAL RELATION WRAPPER
--
--  Wraps public.principals to make it updatable, and produce
--  nice error messages when an integrity constraint is violated. Note
--  that you still have to declare public.principals__mutate(varchar,
--  varchar[], int, public.principals,  public.principals)
--  BEFORE including this macro.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.principals__mutate()
RETURNS TRIGGER AS
$$
BEGIN
    RETURN public.principals__mutate(TG_OP, TG_ARGV, TG_NARGS,
        TG_TABLE_SCHEMA, TG_TABLE_NAME,
        CASE WHEN TG_OP = 'INSERT' THEN NULL ELSE OLD END,
        CASE WHEN TG_OP = 'DELETE' THEN NULL ELSE NEW END
    );
END;
$$ LANGUAGE PLPGSQL;


DROP TRIGGER IF EXISTS mutate ON public.principals CASCADE;
CREATE TRIGGER mutate
    INSTEAD OF INSERT OR UPDATE OR DELETE
    ON public.principals
    FOR EACH ROW EXECUTE PROCEDURE
    public.principals__mutate();

-----------------------------------------------------------------------
--  End trigger procedure public.principals__mutate()
-----------------------------------------------------------------------


-- The historical state view for PRINCIPAL entities.
CREATE VIEW state.principals AS
    SELECT
        M.mutation_timestamp,
        M.mutation_principal,
        M.mutation_client,
        M.principal_id,
        R1.subtype,
        R1.date_registered,
        R2.is_active,
        R3.is_deleted,
        COALESCE(R4.email_address, '') AS email_address,
        COALESCE(R5.username, '') AS username
    FROM entities.principals R1
    JOIN state.principals_mutations M ON
        R1.principal_id = M.principal_id
    JOIN state.principals_is_active R2 ON
        R1.principal_id = R2.principal_id AND
        R2.transaction_time @> M.mutation_timestamp::timestamp with time zone
    JOIN state.principals_is_deleted R3 ON
        R1.principal_id = R3.principal_id AND
        R3.transaction_time @> M.mutation_timestamp::timestamp with time zone
    LEFT OUTER JOIN state.principals_email_address R4 ON
        R1.principal_id = R4.principal_id AND
        R4.transaction_time @> M.mutation_timestamp::timestamp with time zone
    LEFT OUTER JOIN state.principals_username R5 ON
        R1.principal_id = R5.principal_id AND
        R5.transaction_time @> M.mutation_timestamp::timestamp with time zone
    ORDER BY M.mutation_timestamp, R1.principal_id;


CREATE VIEW public.credentials AS
    SELECT
        R1.principal_id,
        R2.passphrase
    FROM
        entities.principals R1
    JOIN state.principals_passphrase R2 ON
        R1.principal_id = R2.principal_id AND
        R2.transaction_time @> public.get_session_state_timestamp();


-----------------------------------------------------------------------
--  Mutation procedure for public.credentials
--
--  A mutation procedure should make the following state changes:
--
--  -   Insert into state.credentials_mutations
--      (if applicable).
--  -   Insert or update the underlying base relations.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.credentials__mutate(
    TG_OP varchar,
    TG_ARGV varchar[],
    TG_NARGS int,
    TG_TABLE_SCHEMA name,
    TG_TABLE_NAME name,
    OLD public.credentials,
    NEW public.credentials
)
RETURNS public.credentials AS
$$
DECLARE
    obj public.credentials;
BEGIN
    -- Bail out early if the record was not changed.
    IF TG_OP = 'UPDATE' AND NEW IS NOT DISTINCT FROM OLD THEN
        RETURN NEW;
    END IF;
    obj := CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
    IF NOT state.principals_is_mutated(obj.principal_id) THEN
        PERFORM state.principals_create_mutation(obj.principal_id);
    END IF;
    CASE
        WHEN TG_OP IN ('INSERT','UPDATE') THEN
            IF COALESCE(obj.passphrase, '') != ''
            AND (
                obj.passphrase IS DISTINCT FROM OLD.passphrase
                OR TG_OP = 'INSERT'
            ) THEN
                INSERT INTO state.principals_passphrase
                    (principal_id, passphrase)
                VALUES (obj.principal_id, obj.passphrase);
            END IF;
        WHEN TG_OP = 'DELETE' THEN
            UPDATE state.principals_passphrase SET
                transaction_time = tstzrange(
                    lower(transaction_time),
                    public.get_session_state_timestamp()
                )
            WHERE
                principal_id = obj.principal_id AND
                transaction_time @> public.get_session_state_timestamp();
        ELSE
            RAISE invalid_parameter_value USING
                MESSAGE = format('Invalid TG_OP: %s', TG_OP),
                HINT = format('Use either INSERT, UPDATE, DELETE or TRUNCATE');
    END CASE;
    RETURN obj;
END;
$$ LANGUAGE PLPGSQL SECURITY INVOKER;

-----------------------------------------------------------------------
--  End mutation procedure public.credentials__mutate()
-----------------------------------------------------------------------


-----------------------------------------------------------------------
--  UPDATABLE VIRTUAL RELATION WRAPPER
--
--  Wraps public.credentials to make it updatable, and produce
--  nice error messages when an integrity constraint is violated. Note
--  that you still have to declare public.credentials__mutate(varchar,
--  varchar[], int, public.credentials,  public.credentials)
--  BEFORE including this macro.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.credentials__mutate()
RETURNS TRIGGER AS
$$
BEGIN
    RETURN public.credentials__mutate(TG_OP, TG_ARGV, TG_NARGS,
        TG_TABLE_SCHEMA, TG_TABLE_NAME,
        CASE WHEN TG_OP = 'INSERT' THEN NULL ELSE OLD END,
        CASE WHEN TG_OP = 'DELETE' THEN NULL ELSE NEW END
    );
END;
$$ LANGUAGE PLPGSQL;


DROP TRIGGER IF EXISTS mutate ON public.credentials CASCADE;
CREATE TRIGGER mutate
    INSTEAD OF INSERT OR UPDATE OR DELETE
    ON public.credentials
    FOR EACH ROW EXECUTE PROCEDURE
    public.credentials__mutate();

-----------------------------------------------------------------------
--  End trigger procedure public.credentials__mutate()
-----------------------------------------------------------------------


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  SOUSOU IDENTITY MANAGEMENT SYSTEM INITIAL DATA
--
--  This file specifies the initial data for the Sousou IMS database
--  schema, such as the root user and clients.
--
-----------------------------------------------------------------------

SELECT public.set_session_user(0);
SELECT public.set_session_client(0);
SELECT public.set_session_mutation_timestamp('2011-01-01 00:00+00');


-- entities.clients initial data
WITH
clients (client_id, codename, display_name) AS (
    VALUES
        (-2, 'unspecified', 'Unspecified'),
        (-1, 'anonymous', 'Anonymous'),
        (0, 'tngems', 'TNG Enterprise Management System')
)
INSERT INTO entities.clients
    (client_id, codename)
SELECT client_id, codename
FROM clients
WHERE codename NOT IN (
    SELECT codename
    FROM entities.clients
);


-- These are the default users specified in The Sovereign Charter
WITH
users (user_id, subtype, username, date_registered) AS (
    VALUES
        (0, 'auto', 'root', '2011-01-01 00:00:00'),
        (1, 'auto', 'fulcrum', '2011-01-01 00:00:00'),
        (2, 'auto', 'neural', '2011-01-01 00:00:00'),
        (3, 'auto', 'commander', '2011-01-01 00:00:00'),
        (4, 'auto', 'sousou', '2011-01-01 00:00:00'),
        (-1, 'auto', 'anonymous', '2011-01-01 00:00:00'),
        (-2, 'auto', 'unspecified', '2011-01-01 00:00:00')
)
INSERT INTO public.principals
    (principal_id, subtype, username, date_registered, is_active)
SELECT user_id, subtype, username, date_registered::timestamp with time zone,
    TRUE
FROM users
WHERE username NOT IN (
    SELECT username
    FROM public.principals
);



-- Important!
SELECT public.set_session_mutation_timestamp(CURRENT_TIMESTAMP);


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  CASANOVA FILE STORAGE SYSTEM DATA DEFINITION LANGUAGE
--
--  The Casanova Centralized Filestorage System (CFS) provides a library of
--  all static files owned and managed by the enterprise.
--
--  The Casanova CFS specifies the following entities:
--
--  -   Bucket
--  -   Index Node
--  -   Image Index Node
--  -   Audio Index Node
--
-----------------------------------------------------------------------
DROP TABLE IF EXISTS entities.buckets CASCADE;
DROP TABLE IF EXISTS entities.inodes CASCADE;
DROP TABLE IF EXISTS entities.inodes_audio CASCADE;
DROP TABLE IF EXISTS entities.inodes_image CASCADE;


-----------------------------------------------------------------------
--  BUCKET
--
--  A BUCKET represents a container where files are stored in.
--
--  Columns:
--      bucket_type: specifies the bucket type.
--      bucket_id: a surrogate primary key.
--      identifier: a mnemmonic key.
--      public_access: indicates if public access is globally enabled or
--          disabled.
--      unmanaged: indicates if the bucket is unmanaged. Unmanaged buckets
--          have no INDEX NODEs associated with them.
--      quota: specifies the maximum size of the bucket, in bytes.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.buckets(
    bucket_type varchar NOT NULL,
    bucket_id int8 NOT NULL,
    identifier varchar NOT NULL,
    public_access boolean NOT NULL
        DEFAULT FALSE,
    unmanaged boolean NOT NULL
        DEFAULT FALSE,
    quota int8 NOT NULL
        DEFAULT 0,
    CONSTRAINT buckets_pk
        PRIMARY KEY (bucket_id),
    CONSTRAINT buckets_ak1
        UNIQUE (identifier),
    CONSTRAINT buckets_quota_gte_zero
        CHECK (quota >= 0)
);


-----------------------------------------------------------------------
--  INDEX NODE
--
--  An INDEX NODE represents a static file managed by the Casanova CFS.
--
--  Columns:
--      inode_id: a surrogate primary key.
--      uuid: a Universally Unique Identifier.
--      subtype: specifies the subtype; generic, audio or video.
--      mimetype: specifies the content type of the file.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.inodes(
    inode_id int8 NOT NULL DEFAULT nextval('tngems_object_id_seq'),
    uuid4 uuid NOT NULL DEFAULT uuid_generate_v4(),
    subtype varchar NOT NULL,
    mimetype varchar NOT NULL,
    filename public.string NOT NULL,
    CONSTRAINT inodes_pk
        PRIMARY KEY (inode_id),
    CONSTRAINT inodes_ak1
        UNIQUE (uuid4)
);


-----------------------------------------------------------------------
--  Inodes Mutation
--
--  Describes a mutation on entities.inodes.
--
--  Columns:
--      mutation_id: a surrogate primary. This column is referenced
--          by the relations holding the historical values of the
--          parent table.
--      principal_id: a reference to the parent table.
--      transaction_time: specifies the period during which the
--          database considered the changeset as a fact.
--      mutation_client: a reference to the entities.clients
--          table specifying the client through which the mutation
--          was issued.
--      mutation_principal: a reference to the entities.inodes
--          table specifying the principal that issued the mutation.
--
-----------------------------------------------------------------------
DROP TABLE IF EXISTS state.inodes_mutations CASCADE;
CREATE TABLE IF NOT EXISTS state.inodes_mutations(
    mutation_id int8 NOT NULL DEFAULT nextval('state.mutations_mutation_id_seq'::regclass),
    inode_id int8 NOT NULL,
    mutation_timestamp public.mutation_timestamp NOT NULL,
    mutation_client public.session_client NOT NULL,
    mutation_principal public.session_user NOT NULL,
    CONSTRAINT inodes_mutations_pk
        PRIMARY KEY (inode_id,mutation_timestamp),
    CONSTRAINT inodes_mutations_ak1 UNIQUE (mutation_id),
    CONSTRAINT inodes_mutations_parent_fk
        FOREIGN KEY (inode_id)
        REFERENCES entities.inodes (inode_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT inodes_mutations_mutation_client_fk
        FOREIGN KEY (mutation_client)
        REFERENCES entities.clients (client_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT inodes_mutations_mutation_principal_fk
        FOREIGN KEY (mutation_principal)
        REFERENCES entities.principals (principal_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED
);


-----------------------------------------------------------------------
--  Return a boolean indicating if a mutation exists for the entity
--  in the current transaction.
--
--  Args:
--      int8: primary key column.
--
--  Returns:
--      boolean
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION state.inodes_is_mutated(int8) RETURNS boolean AS
$$
SELECT EXISTS(
    SELECT 1
    FROM state.inodes_mutations R1
    WHERE
        R1.inode_id = $1 AND
        R1.mutation_timestamp = public.get_session_mutation_timestamp()
);
$$ LANGUAGE SQL STABLE SECURITY DEFINER;


CREATE OR REPLACE FUNCTION state.inodes_is_mutated()
RETURNS TRIGGER AS
$$
BEGIN
    IF NOT state.inodes_is_mutated(NEW.inode_id) THEN
        RAISE integrity_constraint_violation USING
            MESSAGE = format(
                '%s on entities.inodes must create a ' ||
                'state.inodes_mutations instance', TG_OP);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;



-----------------------------------------------------------------------
--  Create a state.inodes_mutations instance.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION state.inodes_create_mutation()
RETURNS TRIGGER AS
$$
BEGIN
    IF NOT state.inodes_is_mutated(NEW.inode_id) THEN
        INSERT INTO state.inodes_mutations
            (inode_id)
        VALUES (NEW.inode_id);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


CREATE OR REPLACE FUNCTION state.inodes_create_mutation(int8)
RETURNS VOID AS
$$
    INSERT INTO state.inodes_mutations
        (inode_id)
    VALUES ($1);
$$ LANGUAGE SQL SECURITY DEFINER;


-- Always create a inodes_mutations instance after INSERT.
DROP TRIGGER IF EXISTS create_mutation_after_insert
    ON entities.inodes;
CREATE TRIGGER create_mutation_after_insert
    AFTER INSERT ON entities.inodes
    FOR EACH ROW EXECUTE PROCEDURE
    state.inodes_create_mutation();


--  States that a INDEX NODE identified by `inode_id` had it's
--  Stateful Attribute Display name set to `display_name` in the period 
--  `transaction_time`.
DROP TABLE IF EXISTS
    state.inodes_display_name CASCADE;
CREATE TABLE IF NOT EXISTS state.inodes_display_name(
    mutation_timestamp public.mutation_timestamp NOT NULL,
    inode_id int8 NOT NULL,
    transaction_time public.transaction_time NOT NULL,
    display_name public.string NOT NULL,
    CONSTRAINT inodes_display_name_pk
        PRIMARY KEY (mutation_timestamp, inode_id),
    CONSTRAINT inodes_display_name_inodes_mutations_fk1
        FOREIGN KEY (mutation_timestamp, inode_id)
        REFERENCES state.inodes_mutations (
            mutation_timestamp, inode_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT inodes_display_name_mutation_timestamp
        CHECK (mutation_timestamp = lower(transaction_time)),
    CONSTRAINT inodes_display_name_transaction_time_excl
        EXCLUDE USING GIST (inode_id WITH =, transaction_time WITH &&),
    CONSTRAINT inodes_display_name_transaction_time_adj
        EXCLUDE USING GIST (
            inode_id WITH =,
            (display_name) WITH =,
            transaction_time WITH -|-
    )
);


-- Update the existing transaction time before inserting.
CREATE OR REPLACE FUNCTION state.inodes_display_name__mutate()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE state.inodes_display_name SET
        transaction_time = tstzrange(lower(transaction_time),
            public.get_session_mutation_timestamp())
    WHERE
        inode_id = NEW.inode_id AND
        transaction_time @> public.get_session_mutation_timestamp();
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


DROP TRIGGER IF EXISTS end_transaction_time
    ON state.inodes_display_name CASCADE;
CREATE TRIGGER end_transaction_time 
    BEFORE INSERT ON state.inodes_display_name
    FOR EACH ROW EXECUTE PROCEDURE 
    state.inodes_display_name__mutate();


--  States that a INDEX NODE identified by `inode_id` had it's
--  Stateful Attribute Checksum set to `content_hash` in the period 
--  `transaction_time`.
DROP TABLE IF EXISTS
    state.inodes_content_hash CASCADE;
CREATE TABLE IF NOT EXISTS state.inodes_content_hash(
    mutation_timestamp public.mutation_timestamp NOT NULL,
    inode_id int8 NOT NULL,
    transaction_time public.transaction_time NOT NULL,
    content_hash varchar(28) NOT NULL,
    CONSTRAINT inodes_content_hash_pk
        PRIMARY KEY (mutation_timestamp, inode_id),
    CONSTRAINT inodes_content_hash_inodes_mutations_fk1
        FOREIGN KEY (mutation_timestamp, inode_id)
        REFERENCES state.inodes_mutations (
            mutation_timestamp, inode_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT inodes_content_hash_mutation_timestamp
        CHECK (mutation_timestamp = lower(transaction_time)),
    CONSTRAINT inodes_content_hash_transaction_time_excl
        EXCLUDE USING GIST (inode_id WITH =, transaction_time WITH &&),
    CONSTRAINT inodes_content_hash_transaction_time_adj
        EXCLUDE USING GIST (
            inode_id WITH =,
            (content_hash) WITH =,
            transaction_time WITH -|-
    )
);


-- Update the existing transaction time before inserting.
CREATE OR REPLACE FUNCTION state.inodes_content_hash__mutate()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE state.inodes_content_hash SET
        transaction_time = tstzrange(lower(transaction_time),
            public.get_session_mutation_timestamp())
    WHERE
        inode_id = NEW.inode_id AND
        transaction_time @> public.get_session_mutation_timestamp();
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


DROP TRIGGER IF EXISTS end_transaction_time
    ON state.inodes_content_hash CASCADE;
CREATE TRIGGER end_transaction_time 
    BEFORE INSERT ON state.inodes_content_hash
    FOR EACH ROW EXECUTE PROCEDURE 
    state.inodes_content_hash__mutate();


--  States that a INDEX NODE identified by `inode_id` had it's
--  Stateful Attribute Filesize set to `filesize` in the period 
--  `transaction_time`.
DROP TABLE IF EXISTS
    state.inodes_filesize CASCADE;
CREATE TABLE IF NOT EXISTS state.inodes_filesize(
    mutation_timestamp public.mutation_timestamp NOT NULL,
    inode_id int8 NOT NULL,
    transaction_time public.transaction_time NOT NULL,
    filesize int8 NOT NULL,
    CONSTRAINT inodes_filesize_pk
        PRIMARY KEY (mutation_timestamp, inode_id),
    CONSTRAINT inodes_filesize_inodes_mutations_fk1
        FOREIGN KEY (mutation_timestamp, inode_id)
        REFERENCES state.inodes_mutations (
            mutation_timestamp, inode_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT inodes_filesize_mutation_timestamp
        CHECK (mutation_timestamp = lower(transaction_time)),
    CONSTRAINT inodes_filesize_transaction_time_excl
        EXCLUDE USING GIST (inode_id WITH =, transaction_time WITH &&),
    CONSTRAINT inodes_filesize_transaction_time_adj
        EXCLUDE USING GIST (
            inode_id WITH =,
            (filesize) WITH =,
            transaction_time WITH -|-
    )
);


-- Update the existing transaction time before inserting.
CREATE OR REPLACE FUNCTION state.inodes_filesize__mutate()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE state.inodes_filesize SET
        transaction_time = tstzrange(lower(transaction_time),
            public.get_session_mutation_timestamp())
    WHERE
        inode_id = NEW.inode_id AND
        transaction_time @> public.get_session_mutation_timestamp();
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


DROP TRIGGER IF EXISTS end_transaction_time
    ON state.inodes_filesize CASCADE;
CREATE TRIGGER end_transaction_time 
    BEFORE INSERT ON state.inodes_filesize
    FOR EACH ROW EXECUTE PROCEDURE 
    state.inodes_filesize__mutate();


--  States that a INDEX NODE identified by `inode_id` had it's
--  Stateful Attribute Policy set to `policy` in the period 
--  `transaction_time`.
DROP TABLE IF EXISTS
    state.inodes_policy CASCADE;
CREATE TABLE IF NOT EXISTS state.inodes_policy(
    mutation_timestamp public.mutation_timestamp NOT NULL,
    inode_id int8 NOT NULL,
    transaction_time public.transaction_time NOT NULL,
    policy varchar NOT NULL,
    CONSTRAINT inodes_policy_pk
        PRIMARY KEY (mutation_timestamp, inode_id),
    CONSTRAINT inodes_policy_inodes_mutations_fk1
        FOREIGN KEY (mutation_timestamp, inode_id)
        REFERENCES state.inodes_mutations (
            mutation_timestamp, inode_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT inodes_policy_mutation_timestamp
        CHECK (mutation_timestamp = lower(transaction_time)),
    CONSTRAINT inodes_policy_transaction_time_excl
        EXCLUDE USING GIST (inode_id WITH =, transaction_time WITH &&),
    CONSTRAINT inodes_policy_transaction_time_adj
        EXCLUDE USING GIST (
            inode_id WITH =,
            (policy) WITH =,
            transaction_time WITH -|-
    )
);


-- Update the existing transaction time before inserting.
CREATE OR REPLACE FUNCTION state.inodes_policy__mutate()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE state.inodes_policy SET
        transaction_time = tstzrange(lower(transaction_time),
            public.get_session_mutation_timestamp())
    WHERE
        inode_id = NEW.inode_id AND
        transaction_time @> public.get_session_mutation_timestamp();
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


DROP TRIGGER IF EXISTS end_transaction_time
    ON state.inodes_policy CASCADE;
CREATE TRIGGER end_transaction_time 
    BEFORE INSERT ON state.inodes_policy
    FOR EACH ROW EXECUTE PROCEDURE 
    state.inodes_policy__mutate();




-----------------------------------------------------------------------
--  AUDIO INDEX NODE
--
--  Represents an INDEX NODE holding audio data.
--
--  Columns:
--      inode_id: a reference to the entities.inodes 
--          relation.
--      acodec: identifies the codec that was used to encode the raw
--          audio.
--      channels: the number of channels in the recording (0 if not
--          known).
--      duration: the duration, in milliseconds.
--      samplerate: the samplerate of the recording, in Herz/second.
--      bitrate: the bitrate of the recording, in kB/second.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.inodes_audio(
    inode_id int8 NOT NULL,
    acodec varchar NOT NULL,
    channels int NOT NULL,
    duration int8 NOT NULL,
    samplerate int NOT NULL,
    bitrate int NOT NULL,
    CONSTRAINT inodes_audio_pk
        PRIMARY KEY (inode_id),
    CONSTRAINT inodes_audio_inodes_fk1
        FOREIGN KEY (inode_id)
        REFERENCES entities.inodes (inode_id)
        ON UPDATE CASCADE ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT inodes_audio_channels_gte_zero
        CHECK (channels >= 0),
    CONSTRAINT inodes_audio_duration_gte_zero
        CHECK (duration >= 0),
    CONSTRAINT inodes_audio_samplerate_gte_zero
        CHECK (samplerate >= 0),
    CONSTRAINT inodes_audio_bitrate_gte_zero
        CHECK (bitrate >= 0)
);


-----------------------------------------------------------------------
--  IMAGE INDEX NODE
--
--  Represents an IMAGE INDEX NODE holding image data.
--
--  Column:
--      inode_id: reference to the entities.inodes
--          relation.
--      icodec: identifies the codec that was used to encode the image.
--      pixel_format: specifies the pixel format of the encoded image
--          data.
--      width: the width of the image, in pixels.
--      height: the height of the image, in pixels.
--      luma: the luma.
--      center: coordinates of the image subject, represented as two
--          floating point values in [0.0,1.0].
--   
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.inodes_image(
    inode_id int8 NOT NULL,
    icodec varchar NOT NULL,
    pixel_format varchar NOT NULL,
    width int NOT NULL,
    height int NOT NULL,
    luma double precision NOT NULL,
    center double precision[] NOT NULL,
    CONSTRAINT inodes_image_pk
        PRIMARY KEY (inode_id),
    CONSTRAINT inodes_image_inodes_fk1
        FOREIGN KEY (inode_id)
        REFERENCES entities.inodes (inode_id)
        ON UPDATE CASCADE ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT inodes_image_width_gt_zero
        CHECK (width > 0),
    CONSTRAINT inodes_image_height_gt_zero
        CHECK (height > 0),
    CONSTRAINT inodes_image_center1_in_0_1
        CHECK (center[1] IS NOT NULL AND numrange(0.0, 1.0, '[]') @> center[1]::numeric),
    CONSTRAINT inodes_image_center2_in_0_1
        CHECK (center[2] IS NOT NULL AND numrange(0.0, 1.0, '[]') @> center[2]::numeric),
    CONSTRAINT inodes_image_pixel_format_valid
        CHECK (pixel_format IN (
            'RGB',
            'RGBA',
            'RGBX',
            'RGBa',
            'CMYK',
            'YCbCr',
            '1',
            'P',
            'L',
            'LA',
            'I',
            'F'
        )
    )
);


-----------------------------------------------------------------------
--  INODE DESCRIPTOR
--
--  Identifies the physical location of an INDEX NODE.
--
--  Columns:
--      bucket: identifies the BUCKET holding the file.
--      inode_id: a reference to the entities.inodes
--          relation.
--      storage_key: the local path specification in the BUCKET.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.inodedescriptors(
    bucket varchar NOT NULL,
    inode_id int8 NOT NULL,
    storage_key varchar NOT NULL,
    CONSTRAINT inodedescriptors_pk
        PRIMARY KEY (bucket, storage_key),
    CONSTRAINT inodedescriptors_buckets_fk1
        FOREIGN KEY (bucket)
        REFERENCES entities.buckets (identifier)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT inodedescriptors_inodes_fk1
        FOREIGN KEY (inode_id)
        REFERENCES entities.inodes (inode_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE
        
);


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  COMMUNICATION  DDL, VIEWS, PROCEDURES AND TRIGGERS
--
-----------------------------------------------------------------------
DROP TABLE IF EXISTS
    common.contactmechanismtypes CASCADE;
DROP TABLE IF EXISTS
    entities.contactmechanisms CASCADE;
DROP TABLE IF EXISTS
    entities.emailaddresses CASCADE;
DROP TABLE IF EXISTS
    entities.phonenumbers CASCADE;
DROP TABLE IF EXISTS
    common.contactmechanismapplicationtypes CASCADE;
DROP TABLE IF EXISTS
    common.contactmechanismapplications CASCADE;



-----------------------------------------------------------------------
--  COMMUNICATION MECHANISM TYPE
--
--  Specifies a type of communcation mechanism.
--
--  Columns:
--      code: an identifier.
--      description: a description/label.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS common.contactmechanismtypes(
    code public.string NOT NULL,
    description public.string NOT NULL,
    CONSTRAINT contactmechanismtypes_pk
        PRIMARY KEY (code)
);


-----------------------------------------------------------------------
--  CONTACT MECHANISM APPLICATION TYPE
--
--  Specifies a type of application for a contact mechanism.
--
--  Columns:
--      mechanism_type: the contact mechanism type.
--      code: the contact mechanism applicatio code.
--      description: a short description.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS common.contactmechanismapplicationtypes(
    mechanism_type varchar NOT NULL,
    code public.string NOT NULL,
    description public.string NOT NULL,
    CONSTRAINT contactmechanismapplicationtypes_pk
        PRIMARY KEY (mechanism_type, code),
    CONSTRAINT contactmechanismapplicationtypes_contactmechanismtypes_fk1
        FOREIGN KEY (mechanism_type)
        REFERENCES common.contactmechanismtypes (code)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE
);


-----------------------------------------------------------------------
--  CONTACT MECHANISM
--
--  Represents a mechanism through which a party can be contacted.
--
--  Columns:
--      mechanism_type: identifiers the type of contact mechanism.
--      mechanism_id: a surrogate primary key.
--
--  Notes:
--  -   Clients MUST NOT insert on this table. Mutations on
--      entities.contactmechanism MUST occur through
--      one of it's child tables (e.g. entities.emailaddresses,
--      entities.phonenumbers).
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.contactmechanisms(
    mechanism_type varchar NOT NULL,
    mechanism_id int8 NOT NULL,
    CONSTRAINT contactmechanisms_pk
        PRIMARY KEY (mechanism_type, mechanism_id)
);



-----------------------------------------------------------------------
--  CONTACT MECHANISM APPLICATION
--
--  Specifies the possible applications of a contact mechanism.
--
--  Columns:
--      mechanism_type: identifiers the type of contact mechanism.
--      mechanism_id: the mechanism id.
--      application_type: the application type.
--      during: the period during which the application was used.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.contactmechanismapplications(
    mechanism_type varchar NOT NULL,
    mechanism_id int8 NOT NULL,
    during public.transaction_time NOT NULL
        DEFAULT tstzrange(CURRENT_TIMESTAMP, 'infinity'),
    application_type varchar NOT NULL,
    CONSTRAINT contactmechanismapplications_pk
        PRIMARY KEY (mechanism_type, mechanism_id, during, application_type),
    CONSTRAINT contactmechanismapplications_excl
        EXCLUDE USING GIST (mechanism_type WITH =, mechanism_id WITH =,
            during WITH &&, application_type WITH =),
    CONSTRAINT contactmechanismapplications_adj
        EXCLUDE USING GIST (mechanism_type WITH =, mechanism_id WITH =,
            during WITH -|-, application_type WITH =),
    CONSTRAINT contactmechanismapplications_contactmechanisms_fk1
        FOREIGN KEY (mechanism_type,mechanism_id)
        REFERENCES entities.contactmechanisms (mechanism_type, mechanism_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT contactmechanismapplications_contactmechanismapplicationtypes_fk2
        FOREIGN KEY (mechanism_type, application_type)
        REFERENCES common.contactmechanismapplicationtypes (mechanism_type, code)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE
);


-----------------------------------------------------------------------
--  EMAIL ADDRESS
--
--  Specifies an e-mail address.
--
--  Columns:
--      email_address: the email address.
--      is_suspended: indicates if automated mail to this e-mail address
--          is suspended.
--      is_blocked: indicates if incoming mail from this e-mail address
--          should be blocked.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.emailaddresses(
    mechanism_type varchar NOT NULL,
    mechanism_id int8 NOT NULL,
    email_address varchar NOT NULL,
    is_valid boolean NOT NULL DEFAULT FALSE,
    is_suspended boolean NOT NULL DEFAULT FALSE,
    is_blocked boolean NOT NULL DEFAULT FALSE,
    CONSTRAINT emailaddresses_pk
        PRIMARY KEY (email_address),
    CONSTRAINT emailaddresses_ak1
        UNIQUE (mechanism_type, mechanism_id),
    CONSTRAINT emailaddresses_contactmechanisms_fk1
        FOREIGN KEY (mechanism_type, mechanism_id)
        REFERENCES entities.contactmechanisms (mechanism_type, mechanism_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE
);


ALTER TABLE entities.emailaddresses ALTER COLUMN mechanism_type
    SET DEFAULT 'email';
ALTER TABLE entities.emailaddresses DROP CONSTRAINT IF EXISTS
    emailaddresses_mechanism_type_chk CASCADE;
ALTER TABLE entities.emailaddresses ADD CONSTRAINT emailaddresses_mechanism_type_chk
    CHECK (mechanism_type = 'email');
ALTER TABLE entities.emailaddresses DROP CONSTRAINT IF EXISTS
    emailaddresses_ak1 CASCADE;
ALTER TABLE entities.emailaddresses ADD CONSTRAINT emailaddresses_ak1
    UNIQUE (mechanism_id);
ALTER TABLE entities.emailaddresses ALTER COLUMN mechanism_id
    SET DEFAULT nextval('tngems_object_id_seq');





-----------------------------------------------------------------------
--  PHONENUMBER
--
--  Specifies an ITU-T E.164 formatted international phonenumber.
--
--  Columns:
--      phonenumber: the phonenumber.
--      line_type: specifies the line type; (L)andline, (M)obile
--          or (U)nknown.
--      is_valid: indicates if the phonenumber is confirmed valid.
--      is_suspended: indicates if automated calling is suspended.
--      is_blocked: indicates if incoming calls from this phonenumber
--          should be blocked.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.phonenumbers(
    mechanism_type varchar NOT NULL,
    mechanism_id int8 NOT NULL,
    phonenumber public.phonenumber NOT NULL,
    line_type varchar(1) NOT NULL DEFAULT 'U',
    is_valid boolean NOT NULL DEFAULT FALSE,
    is_suspended boolean NOT NULL DEFAULT FALSE,
    is_blocked boolean NOT NULL DEFAULT FALSE,
    CONSTRAINT phonenumbers_pk
        PRIMARY KEY (phonenumber),
    CONSTRAINT phonenumbers_line_type_valid
        CHECK (line_type IN ('L','M','U')),
    CONSTRAINT phonenumbers_ak1
        UNIQUE (mechanism_type, mechanism_id),
    CONSTRAINT phonenumbers_contactmechanisms_fk1
        FOREIGN KEY (mechanism_type, mechanism_id)
        REFERENCES entities.contactmechanisms (mechanism_type, mechanism_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE
);


ALTER TABLE entities.phonenumbers ALTER COLUMN mechanism_type
    SET DEFAULT 'phonenumber';
ALTER TABLE entities.phonenumbers DROP CONSTRAINT IF EXISTS
    phonenumbers_mechanism_type_chk CASCADE;
ALTER TABLE entities.phonenumbers ADD CONSTRAINT phonenumbers_mechanism_type_chk
    CHECK (mechanism_type = 'phonenumber');
ALTER TABLE entities.phonenumbers DROP CONSTRAINT IF EXISTS
    phonenumbers_ak1 CASCADE;
ALTER TABLE entities.phonenumbers ADD CONSTRAINT phonenumbers_ak1
    UNIQUE (mechanism_id);
ALTER TABLE entities.phonenumbers ALTER COLUMN mechanism_id
    SET DEFAULT nextval('tngems_object_id_seq');



-----------------------------------------------------------------------
--
--  CONTACT MECHANISM PROCEDURES
--
-----------------------------------------------------------------------


-----------------------------------------------------------------------
--  Idempotently set the applications for a contact mechanism.
--
--  Args:
--      varchar: the mechanism type.
--      int8: the mechanism id.
--      varchar[]: the applications.
--
--  Returns:
--      int
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.contact_set_mechanism_applications(
    varchar, int8, varchar[])
RETURNS int8 AS
$$
    WITH insert_applications(mechanism_type, mechanism_id, application_type) AS (
        INSERT INTO entities.contactmechanismapplications
            (mechanism_type, mechanism_id, application_type)
        SELECT $1, $2, application_type
        FROM unnest($3) application_type
        WHERE ($1, $2, application_type) NOT IN (
            SELECT mechanism_type, mechanism_id, application_type
            FROM entities.contactmechanismapplications L1
            WHERE
                L1.mechanism_type = $1 AND
                L1.mechanism_id = $2 AND
                L1.application_type = application_type AND
                L1.during @> CURRENT_TIMESTAMP
        )
        RETURNING mechanism_type, mechanism_id, application_type
    )
    SELECT COUNT(*) FROM insert_applications;
$$ LANGUAGE SQL SECURITY DEFINER;


-----------------------------------------------------------------------
--  Idempotently set the applications for a contact mechanism.
--
--  Args:
--      entities.contactmechanisms: the contact mechanism.
--      varchar[]: the applications.
--
--  Returns:
--      int
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.contact_set_mechanism_applications(
    entities.contactmechanisms, varchar[])
RETURNS int8 AS
$$
    SELECT * FROM public.contact_set_mechanism_applications(
        $1.mechanism_type, $1.mechanism_id, $2);
$$ LANGUAGE SQL SECURITY DEFINER;


-----------------------------------------------------------------------
--  Idempotently get or create a phonenumber.
--
--  Args:
--      varchar: the phonenumber.
--      varchar[]: applications of the phonenumber.
--
--  Returns:
--      record(varchar, int)
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.contact_get_or_create_phonenumber(
    varchar, varchar[] DEFAULT ARRAY[]::varchar[])
RETURNS entities.contactmechanisms AS
$$
DECLARE
    result entities.contactmechanisms;
BEGIN
    SELECT mechanism_type, mechanism_id INTO result
    FROM entities.phonenumbers
    WHERE phonenumber = $1;
    IF NOT FOUND THEN
        INSERT INTO entities.contactmechanisms (mechanism_type, mechanism_id)
        VALUES ('phonenumber', nextval('entities.phonenumbers_mechanism_id_seq'))
        RETURNING mechanism_type, mechanism_id INTO result;
        INSERT INTO entities.phonenumbers (mechanism_id, phonenumber)
        VALUES (result.mechanism_id, $1);
    END IF;
    PERFORM public.contact_set_mechanism_applications(result, $2);
    RETURN result;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


-----------------------------------------------------------------------
--  Idempotently get or create a email_address.
--
--  Args:
--      varchar: the email_address.
--      varchar[]: applications of the email_address.
--
--  Returns:
--      record(varchar, int)
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.contact_get_or_create_emailaddress(
    varchar, varchar[] DEFAULT ARRAY[]::varchar[])
RETURNS entities.contactmechanisms AS
$$
DECLARE
    result entities.contactmechanisms;
BEGIN
    SELECT mechanism_type, mechanism_id INTO result
    FROM entities.emailaddresses
    WHERE email_address = $1;
    IF NOT FOUND THEN
        INSERT INTO entities.contactmechanisms (mechanism_type, mechanism_id)
        VALUES ('email', nextval('entities.emailaddresses_mechanism_id_seq'))
        RETURNING mechanism_type, mechanism_id INTO result;
        INSERT INTO entities.emailaddresses (mechanism_id, email_address)
        VALUES (result.mechanism_id, $1);
    END IF;
    PERFORM public.contact_set_mechanism_applications(result, $2);
    RETURN result;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


-----------------------------------------------------------------------
--
--  CONTACT VIRTUAL RELATIONS
--
-----------------------------------------------------------------------
DROP VIEW IF EXISTS public.phonenumbers CASCADE;
DROP VIEW IF EXISTS public.emailaddresses CASCADE;


-----------------------------------------------------------------------
--  BEGIN PUBLIC.PHONENUMBERS
-----------------------------------------------------------------------
CREATE VIEW public.phonenumbers AS
    SELECT
        R1.mechanism_type,
        R1.mechanism_id,
        COALESCE(R2.applications, ARRAY[]::text[]) AS applications,
        R1.phonenumber,
        R1.line_type,
        R1.is_valid,
        R1.is_suspended,
        R1.is_blocked
    FROM entities.phonenumbers R1
    LEFT OUTER JOIN (
        SELECT mechanism_type, mechanism_id, array_agg(application_type) AS applications
        FROM entities.contactmechanismapplications
        GROUP BY mechanism_type, mechanism_id
    ) R2 ON
        R1.mechanism_type = R2.mechanism_type AND
        R1.mechanism_id = R2.mechanism_id;


-----------------------------------------------------------------------
--  END PUBLIC.PHONENUMBERS
-----------------------------------------------------------------------



-----------------------------------------------------------------------
--  BEGIN PUBLIC.EMAILADDRESSES
-----------------------------------------------------------------------
CREATE VIEW public.emailaddresses AS
    SELECT
        R1.mechanism_type,
        R1.mechanism_id,
        COALESCE(R2.applications, ARRAY[]::text[]) AS applications,
        R1.email_address,
        R1.is_valid,
        R1.is_suspended,
        R1.is_blocked
    FROM entities.emailaddresses R1
    LEFT OUTER JOIN (
        SELECT mechanism_type, mechanism_id, array_agg(application_type) AS applications
        FROM entities.contactmechanismapplications
        GROUP BY mechanism_type, mechanism_id
    ) R2 ON
        R1.mechanism_type = R2.mechanism_type AND
        R1.mechanism_id = R2.mechanism_id;


-----------------------------------------------------------------------
--  END PUBLIC.EMAILADDRESSES
-----------------------------------------------------------------------


-----------------------------------------------------------------------
--
--  CONTACT MECHANISM INITIAL DATA
--
-----------------------------------------------------------------------


WITH
contactmechanismtypes(code, description) AS (
    VALUES
        ('phonenumber', 'Phonenumber'),
        ('email', 'E-mail address'),
        ('postal', 'Postal address'),
        ('website', 'Website'),
        ('unknown', 'Unknown'),
        ('live', 'Live')
),
upsert AS (
    UPDATE common.contactmechanismtypes R SET
        description = U.description
    FROM contactmechanismtypes U
    WHERE
        R.code = U.code
    RETURNING R.*
)
INSERT INTO common.contactmechanismtypes
    (code, description)
SELECT R.code, description
FROM contactmechanismtypes R
WHERE R.code NOT IN (
    SELECT U.code
    FROM upsert U
    WHERE U.code = R.code
);


WITH
contactmechanismapplicationtypes(mechanism_type, code, description) AS (
    VALUES
        ('phonenumber', 'voice', 'Phone'),
        ('phonenumber', 'fax', 'Fax'),
        ('phonenumber', 'sms', 'Short Message Service (SMS)'),
        ('phonenumber', 'whatsapp', 'WhatsApp'),
        ('phonenumber', 'tango', 'Tango'),
        ('phonenumber', 'facebook', 'Facebook Messenger'),
        ('phonenumber', 'viber', 'Viber'),
        ('phonenumber', 'skype', 'Skype'),
        ('email', 'email', 'Email'),
        ('email', 'skype', 'Skype'),
        ('website', 'chat', 'Live chat'),
        ('website', 'message', 'Direct message'),
        ('website', 'form', 'Contact form'),
        ('website', 'comments', 'Comments'),
        ('unknown', 'unknown', 'Unknown')
),
upsert AS (
    UPDATE common.contactmechanismapplicationtypes R SET
        description = U.description
    FROM contactmechanismapplicationtypes U
    WHERE
        R.code = U.code AND
        R.mechanism_type = U.mechanism_type
    RETURNING R.*
)
INSERT INTO common.contactmechanismapplicationtypes
    (mechanism_type, code, description)
SELECT R.mechanism_type, code, description
FROM contactmechanismapplicationtypes R
WHERE (R.mechanism_type, R.code) NOT IN (
    SELECT U.mechanism_type, U.code
    FROM upsert U
    WHERE U.code = R.code
);


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  PARTY DATA DEFINITION LANGUAGE (DDL)
--
--  The PARTY schema specifies a datamodel to store details about
--  entities with whom an organization transacts, such as 
--  classifications, contact mechanisms and commnunication events.
--
--  The PARTY entity is the base entity for all other entities 
--  involving natural persons or legal entities.
--
-----------------------------------------------------------------------
DROP TABLE IF EXISTS
    entities.party CASCADE;


-----------------------------------------------------------------------
--  PARTY
--
--  Represents an entity with whom an organization transacts, e.g. a
--  natural person or legal entity.
--
--  Columns:
--      party_id: a surrogate primary key.
--      subtype: a discriminator column, distuinguishing between
--          NATURAL PERSONs and LEGAL ENTITYs.
--      identifier: a mnemmonic identifier.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.party(
    party_id int8 NOT NULL
        DEFAULT nextval('tngems_object_id_seq'),
    subtype varchar(1) NOT NULL,
    CONSTRAINT party_pk
        PRIMARY KEY (party_id)
);


-----------------------------------------------------------------------
--  Party Mutation
--
--  Describes a mutation on entities.party.
--
--  Columns:
--      mutation_id: a surrogate primary. This column is referenced
--          by the relations holding the historical values of the
--          parent table.
--      principal_id: a reference to the parent table.
--      transaction_time: specifies the period during which the
--          database considered the changeset as a fact.
--      mutation_client: a reference to the entities.clients
--          table specifying the client through which the mutation
--          was issued.
--      mutation_principal: a reference to the entities.party
--          table specifying the principal that issued the mutation.
--
-----------------------------------------------------------------------
DROP TABLE IF EXISTS state.party_mutations CASCADE;
CREATE TABLE IF NOT EXISTS state.party_mutations(
    mutation_id int8 NOT NULL DEFAULT nextval('state.mutations_mutation_id_seq'::regclass),
    party_id int8 NOT NULL,
    mutation_timestamp public.mutation_timestamp NOT NULL,
    mutation_client public.session_client NOT NULL,
    mutation_principal public.session_user NOT NULL,
    CONSTRAINT party_mutations_pk
        PRIMARY KEY (party_id,mutation_timestamp),
    CONSTRAINT party_mutations_ak1 UNIQUE (mutation_id),
    CONSTRAINT party_mutations_parent_fk
        FOREIGN KEY (party_id)
        REFERENCES entities.party (party_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT party_mutations_mutation_client_fk
        FOREIGN KEY (mutation_client)
        REFERENCES entities.clients (client_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT party_mutations_mutation_principal_fk
        FOREIGN KEY (mutation_principal)
        REFERENCES entities.principals (principal_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED
);


-----------------------------------------------------------------------
--  Return a boolean indicating if a mutation exists for the entity
--  in the current transaction.
--
--  Args:
--      int8: primary key column.
--
--  Returns:
--      boolean
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION state.party_is_mutated(int8) RETURNS boolean AS
$$
SELECT EXISTS(
    SELECT 1
    FROM state.party_mutations R1
    WHERE
        R1.party_id = $1 AND
        R1.mutation_timestamp = public.get_session_mutation_timestamp()
);
$$ LANGUAGE SQL STABLE SECURITY DEFINER;


CREATE OR REPLACE FUNCTION state.party_is_mutated()
RETURNS TRIGGER AS
$$
BEGIN
    IF NOT state.party_is_mutated(NEW.party_id) THEN
        RAISE integrity_constraint_violation USING
            MESSAGE = format(
                '%s on entities.party must create a ' ||
                'state.party_mutations instance', TG_OP);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;



-----------------------------------------------------------------------
--  Create a state.party_mutations instance.
--
-----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION state.party_create_mutation()
RETURNS TRIGGER AS
$$
BEGIN
    IF NOT state.party_is_mutated(NEW.party_id) THEN
        INSERT INTO state.party_mutations
            (party_id)
        VALUES (NEW.party_id);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


CREATE OR REPLACE FUNCTION state.party_create_mutation(int8)
RETURNS VOID AS
$$
    INSERT INTO state.party_mutations
        (party_id)
    VALUES ($1);
$$ LANGUAGE SQL SECURITY DEFINER;


-- Always create a party_mutations instance after INSERT.
DROP TRIGGER IF EXISTS create_mutation_after_insert
    ON entities.party;
CREATE TRIGGER create_mutation_after_insert
    AFTER INSERT ON entities.party
    FOR EACH ROW EXECUTE PROCEDURE
    state.party_create_mutation();


--  States that a PARTY identified by `party_id` had it's
--  Attribute Preferred language set to `preferred_language` in the period 
--  `transaction_time`.
DROP TABLE IF EXISTS
    state.party_preferred_language CASCADE;
CREATE TABLE IF NOT EXISTS state.party_preferred_language(
    mutation_timestamp public.mutation_timestamp NOT NULL,
    party_id int8 NOT NULL,
    transaction_time public.transaction_time NOT NULL,
    preferred_language varchar(3) NOT NULL,
    CONSTRAINT party_preferred_language_pk
        PRIMARY KEY (mutation_timestamp, party_id),
    CONSTRAINT party_preferred_language_partys_mutations_fk1
        FOREIGN KEY (mutation_timestamp, party_id)
        REFERENCES state.party_mutations (
            mutation_timestamp, party_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT party_preferred_language_mutation_timestamp
        CHECK (mutation_timestamp = lower(transaction_time)),
    CONSTRAINT party_preferred_language_transaction_time_excl
        EXCLUDE USING GIST (party_id WITH =, transaction_time WITH &&),
    CONSTRAINT party_preferred_language_transaction_time_adj
        EXCLUDE USING GIST (
            party_id WITH =,
            (preferred_language) WITH =,
            transaction_time WITH -|-
    ),
    CONSTRAINT party_preferred_language_timestamp_eq_lower_tt
        CHECK (mutation_timestamp = lower(transaction_time))
);


-- Update the existing transaction time before inserting.
CREATE OR REPLACE FUNCTION state.party_preferred_language__mutate()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE state.party_preferred_language SET
        transaction_time = tstzrange(lower(transaction_time),
            public.get_session_mutation_timestamp())
    WHERE
        party_id = NEW.party_id AND
        transaction_time @> public.get_session_mutation_timestamp();
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL SECURITY DEFINER;


DROP TRIGGER IF EXISTS end_transaction_time
    ON state.party_preferred_language CASCADE;
CREATE TRIGGER end_transaction_time 
    BEFORE INSERT ON state.party_preferred_language
    FOR EACH ROW EXECUTE PROCEDURE 
    state.party_preferred_language__mutate();



-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  SOUSOU IDENTITY MANAGEMENT SYSTEM INITIAL DATA
--
--  This file specifies the initial data for the Sousou IMS database
--  schema, such as the root user and clients.
--
-----------------------------------------------------------------------
SELECT public.set_session_user(0);
SELECT public.set_session_client(0);
SELECT public.set_session_mutation_timestamp('2011-01-01 00:00+00');


-- entities.party initial data
WITH initial_data(party_id, subtype) AS (
    VALUES
        (-3, 'X'), -- POS
        (-2, 'X'), -- Unspecified
        (-1, 'X') -- Unknown
)
INSERT INTO entities.party (party_id, subtype)
SELECT party_id, subtype
FROM initial_data
WHERE party_id NOT IN (
    SELECT party_id FROM entities.party
);

-- Important!
SELECT public.set_session_mutation_timestamp(CURRENT_TIMESTAMP);


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  PRODUCT DATA DEFINITION LANGUAGE (DDL)
--
--  This file specifies the Data Definition Language (DDL) statements
--  to create a product catalog schema. It stores all information 
--  related to the specification of product (good or services), their
--  pricing (abstract base model) and their descriptions.
--
-----------------------------------------------------------------------
DROP TABLE IF EXISTS
    common.supplierratingtypes CASCADE;
DROP TABLE IF EXISTS
    entities.products CASCADE;
DROP TABLE IF EXISTS
    entities.goods CASCADE;
DROP TABLE IF EXISTS
    entities.services CASCADE;
DROP TABLE IF EXISTS
    entities.reorderguidelines CASCADE;


-----------------------------------------------------------------------
--  SUPPLIER RATING TYPE
--
--  Specifies a rating type for product suppliers.
--
--  Columns:
--      codename: a name identiying the SUPPLIER RATING TYPE.
--      weight: specifies the weight of the rating; ascending.
--
-----------------------------------------------------------------------


-----------------------------------------------------------------------
--  PRODUCT
--
--  Specifies a product that is bought or sold by an enterprise.
--
--  Columns:
--      product_id: a surrogate primary key.
--      product_type: indicates the product type; (G)ood, (S)ervice,
--          or (P)art.
--      manufacturer_id: a reference to the entities.party
--          table identifying the manufacturer, if applicable.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.products(
    product_id int8 NOT NULL
        DEFAULT nextval('tngems_object_id_seq'),
    product_type varchar(1) NOT NULL,
    manufacturer_id int8 NOT NULL
        DEFAULT -2,
    uom varchar NOT NULL,
    CONSTRAINT products_pk
        PRIMARY KEY (product_id),
    CONSTRAINT products_product_type_valid
        CHECK (product_type IN ('G','S','P')),
    CONSTRAINT products_unitsofmeasure_fk1
        FOREIGN KEY (uom)
        REFERENCES common.unitsofmeasure (codename)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE
);


-----------------------------------------------------------------------
--  GOOD
--
--  Represents a PRODUCT of type Good.
--
--  A FINISHED GOOD is a product that is ready to be shipped, and some
--  work may have been performed to get the product to its current state. 
--  A RAW MATERIAL is a component used in making a product in which no 
--  work on it has been performed by the enterprise and it is the lowest 
--  level component that makes up a product. A RAW MATERIAL may be sold 
--  as a good or used in another good. A SUBASSEMBLY good is a product 
--  that is in a state of partial completion and is not generally sold 
--  to a customer or purchased from a supplier. If the enterprise 
--  purchased the subassembly from a supplier, it would be considered 
--  a RAW MATERIAL because the enterprise did not perform any additional 
--  work on the product (Livingston 2001: 100).
--  
--  Columns:
--      product_id: a reference to the entities.products
--          table, identityfing the product.
--      good_type: specifies the type of good; (R)aw material, 
--          (S)ubassembly or (F)inished.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.goods(
    product_id int8 NOT NULL,
    good_type varchar(1) NOT NULL,
    CONSTRAINT goods_pk
        PRIMARY KEY (product_id),
    CONSTRAINT goods_products_fk1
        FOREIGN KEY (product_id)
        REFERENCES entities.products (product_id)
        ON UPDATE CASCADE ON DELETE CASCADE
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT goods_good_type_valid
        CHECK (good_type in ('R','S','F'))
);


-----------------------------------------------------------------------
--  SERVICE
--
--  Represents a PRODUCT of subtype service.
--
--  Columns:
--      product_id: a reference to the entities.products
--          table, identityfing the product.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.services(
    product_id int8 NOT NULL,
    CONSTRAINT services_pk
        PRIMARY KEY (product_id),
    CONSTRAINT services_products_fk1
        FOREIGN KEY (product_id)
        REFERENCES entities.products (product_id)
        ON UPDATE CASCADE ON DELETE CASCADE
        DEFERRABLE INITIALLY IMMEDIATE
);


-----------------------------------------------------------------------
--  REORDER GUIDELINE
--
--  Specifies a default reorder guideline for PRODUCTs of subtype GOOD.
--
--  Columns:
--      product_id: a reference to the entities.goods
--          table, identifying the product for which a reorder
--          guideline is specified.
--      checksum: a checksum of the selection specification(s).
--      during: specifies the period during which the reorder
--          guideline is applicable.
--      reorder_quantity: specifies the amount of the product to
--          reorder in it's default unit of measurement.
--      reorder_level: specifies the minimal stock level for 
--          reordering.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.reorderguidelines(
    id serial NOT NULL,
    checksum varchar(64) NOT NULL,
    product_id int8 NOT NULL,
    during public.transaction_time NOT NULL,
    reorder_quantity int NOT NULL,
    reorder_level int NOT NULL,
    CONSTRAINT reorderguidelines_pk
        PRIMARY KEY (product_id, checksum, during),
    CONSTRAINT reorderguidelines_during_excl
        EXCLUDE USING GIST (product_id WITH =, checksum WITH =, during WITH &&),
    CONSTRAINT reorderguidelines_during_adj
        EXCLUDE USING GIST (product_id WITH =, reorder_quantity WITH =,
            checksum WITH =, reorder_level WITH =, during WITH -|-),
    CONSTRAINT reorderguidelines_goods_fk1
        FOREIGN KEY (product_id)
        REFERENCES entities.goods (product_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT reorderguidelines_reorder_quantity_gt_zero
        CHECK (reorder_quantity > 0),
    CONSTRAINT reorderguidelines_reorder_level_gt_zero
        CHECK (reorder_level > 0)
);


-- depends:auth,party
--
-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  PAYMENT DATA DEFINITION LANGUAGE (DDL)
--
--  This file specifies a schema to store payments and related
--  information.
--
--  Depends:
--      - auth
--      - party
--
-----------------------------------------------------------------------
DROP TABLE IF EXISTS
    common.paymentmethodtypes CASCADE;
DROP TABLE IF EXISTS
    common.paymentserviceproviders CASCADE;
DROP TABLE IF EXISTS
    common.paymentmethods CASCADE;
DROP TABLE IF EXISTS
    entities.payments CASCADE;


-----------------------------------------------------------------------
--  PAYMENT METHOD TYPE
--
--  Represents method through which a payment can occur.
--
--  Columns:
--      codename: an internal identifier.
--      display_name: specifies the display name of the payment method.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS common.paymentmethodtypes(
    codename varchar(32) NOT NULL,
    display_name varchar NOT NULL,
    CONSTRAINT paymentmethodtypes_pk
        PRIMARY KEY (codename)
);


-----------------------------------------------------------------------
--  PAYMENT SERVICE PROVIDER
--
--  Specifies a Payment Service Provider (PSP).
--
--  Columns:
--      codename: an internal identifier.
--      display_name: specifies the display name translation token.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS common.paymentserviceproviders(
    codename varchar(32) NOT NULL,
    display_name varchar NOT NULL,
    CONSTRAINT paymentserviceproviders_pk
        PRIMARY KEY (codename)
);


-----------------------------------------------------------------------
--  PAYMENT METHODS
--
--  Specifies a combination of PAYMENT SERVICE PROVIDER and PAYMENT
--  METHOD TYPE, that can be referenced by PAYMENT entities to indicate
--  the method of payment.
--
--  Columns:
--      service_provider: specifies the PAYMENT SERVICE PROVIDER.
--      payment_method: specifies the PAYMENT METHOD TYPE.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS common.paymentmethods(
    service_provider varchar(32) NOT NULL,
    payment_method varchar(32) NOT NULL,
    CONSTRAINT paymentmethods_pk
        PRIMARY KEY (service_provider, payment_method)
);


-----------------------------------------------------------------------
--  PAYMENT
--
--  Specifies that a payment occurred between two PARTYs at a given
--  date and time, using PAYMENT METHOD T:YPE `payment_method`,
--  facilitated by PAYMENT SERVICE PROVIDER `service_provider`.
--
--  Columns:
--      payment_id: a surrogate primary key.
--      payment_timestamp: specifies the date and time at which the
--          payment occurred (at the consideration of our system).
--      service_provider: specifies the PAYMENT SERVICE PROVIDER that
--          facilitated the payment.
--      payment_method: specifies the PAYMENT METHOD TYPE through which
--          the payment occurred.
--      issuer_id: identifies the PARTY that issued the payment.
--      receiver_id: identifies the PARTY the received the payment.
--      amount: the amount of the payment.
--      currency: the currency of the payment.
--
-----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS entities.payments(
    payment_id serial8 NOT NULL,
    payment_timestamp timestamp with time zone NOT NULL,
    service_provider varchar(32) NOT NULL,
    payment_method varchar(32) NOT NULL,
    issuer_id int NOT NULL,
    receiver_id int NOT NULL,
    amount decimal(19, 6) NOT NULL,
    currency varchar(3) NOT NULL,
    CONSTRAINT payments_pk
        PRIMARY KEY (payment_id),
    CONSTRAINT payments_paymentmethods_fk1
        FOREIGN KEY (service_provider, payment_method)
        REFERENCES common.paymentmethods 
            (service_provider, payment_method)
        ON UPDATE NO ACTION ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT payments_party_fk1
        FOREIGN KEY (issuer_id)
        REFERENCES entities.party (party_id)
        ON UPDATE CASCADE ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT payments_party_fk2
        FOREIGN KEY (receiver_id)
        REFERENCES entities.party (party_id)
        ON UPDATE CASCADE ON DELETE NO ACTION
        DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT payments_amount_gt_zero
        CHECK (amount > '0'::decimal)
);


-- vim: syntax=sql
-----------------------------------------------------------------------
--
--  PAYMENT INITIAL DATA
--
-----------------------------------------------------------------------


-- common.paymentmethodtypes initial data
WITH initial_data(codename, display_name) AS (
    VALUES
        ('cash',            'NAME_PAYMENT_METHOD_TYPE_CASH'),
        ('wire-transfer',   'NAME_PAYMENT_METHOD_TYPE_WIRETRANSFER'),
        ('debitcard',       'NAME_PAYMENT_METHOD_TYPE_DEBITCARD'),
        ('creditcard',      'NAME_PAYMENT_METHOD_TYPE_CREDITCARD'),
        ('check',           'NAME_PAYMENT_METHOD_TYPE_CHECK'),
        ('paypal',          'NAME_PAYMENT_METHOD_TYPE_PAYPAL')
), upsert AS (
    UPDATE common.paymentmethodtypes R1 SET
        display_name = U.display_name
    FROM initial_data U
    WHERE R1.codename = U.codename
    RETURNING R1.*
)
INSERT INTO common.paymentmethodtypes (codename, display_name)
SELECT codename, display_name
FROM initial_data
WHERE codename NOT IN (
    SELECT codename
    FROM upsert
);


COMMIT;
