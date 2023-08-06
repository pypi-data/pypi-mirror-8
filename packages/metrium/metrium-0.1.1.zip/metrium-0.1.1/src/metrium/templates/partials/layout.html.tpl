{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        <title>Metrium / {% block title %}{% endblock %}</title>
    {% endblock %}
</head>
<body class="ux romantic wait-load">
    <div id="overlay" class="overlay"></div>
    <div id="header">
        {% block header %}
            <h1>{% block name %}{% endblock %}</h1>
            <div class="links">
                {% if link == "home" %}
                    <a href="{{ url_for('index') }}" class="active">home</a>
                {% else %}
                    <a href="{{ url_for('index') }}">home</a>
                {% endif %}
                //
                {% if link == "accounts" %}
                    <a href="{{ url_for('list_accounts') }}" class="active">accounts</a>
                {% else %}
                    <a href="{{ url_for('list_accounts') }}">accounts</a>
                {% endif %}
                //
                {% if link == "logs" %}
                    <a href="{{ url_for('list_logs') }}" class="active">log</a>
                {% else %}
                    <a href="{{ url_for('list_logs') }}">log</a>
                {% endif %}
                //
                {% if link == "config" %}
                    <a href="{{ url_for('base_config') }}" class="active">config</a>
                {% else %}
                    <a href="{{ url_for('base_config') }}">config</a>
                {% endif %}
                //
                {% if link == "debug" %}
                    <a href="{{ url_for('list_debug') }}" class="active">debug</a>
                {% else %}
                    <a href="{{ url_for('list_debug') }}">debug</a>
                {% endif %}
            </div>
        {% endblock %}
    </div>
    <div id="content">{% block content %}{% endblock %}</div>
    {% include "partials/footer.html.tpl" %}
</body>
{% include "partials/end_doctype.html.tpl" %}
