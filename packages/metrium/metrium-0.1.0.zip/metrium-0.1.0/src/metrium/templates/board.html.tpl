{% extends "partials/layout_full.html.tpl" %}
{% block title %}Dashboard{% endblock %}
{% block name %}Dashboard{% endblock %}
{% block content %}
    <div class="dashboard">
        <audio class="sound"></audio>
        <div class="video" data-width="1280" data-height="780" data-hd="1"
             data-chromeless="1" data-auto_play="1"></div>
        <div class="pusher" data-key="{{ conf('PUSHER_KEY') }}"></div>
        <div class="header">
            <div class="logo"></div>
            <ul class="sections">
                <li class="active">global</li>
                <li>pendentes</li>
                <li>encomendas</li>
                <li>vendas</li>
                <li>gravações</li>
            </ul>
        </div>
        <div class="message success">
            <span class="author"></span>
            <span class="separator">-</span>
            <span class="contents"></span>
        </div>
        <div class="frame">
            <div class="context">
                <div class="date">
                    <div class="week-day"></div>
                    <div class="day"></div>
                    <div class="time"></div>
                </div>
                <div class="news"></div>
            </div>
            <div class="boards">
                {% include "boards/global.html.tpl" %}
                {% include "boards/pending.html.tpl" %}
            </div>
        </div>
    </div>
{% endblock %}
