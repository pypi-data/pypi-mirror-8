

{% macro is_not_default(varname, default) %}
COALESCE({{ varname }}, {{ default }}) != {{ default }}
{%- endmacro %}
