<%inherit file="base.mako" />

<%!
    import flask

    from git_code_debt.util.iter import chunk_iter
%>

<%block name="title">Graph - ${metric_name}</%block>

<%block name="scripts">
    ${parent.scripts()}
    <script src="/static/js/jquery.flot.min.js"></script>
    <script src="/static/js/jquery.flot.selection.min.js"></script>
    <script src="/static/js/jquery.flot.time.min.js"></script>
    <script src="/static/js/graph.js"></script>
</%block>

<script>
    metrics = ${metrics};
</script>

<h1>${metric_name}</h1>
<div id="graph" style="width: 900px; height: 600px;"></div>
<div class="date-picker">
    <form action="${flask.url_for('graph.all_data', metric_name=metric_name)}" method="GET" style="display: inline-block">
       <input type="submit" value="All Data">
    </form>
    From: <input type="text" id="datepicker-from" data-timestamp="${start_timestamp}">
    To: <input type="text" id="datepicker-to" data-timestamp="${end_timestamp}">
</div>


<h2>Changes</h2>
<div class="changes-container" data-ajax-url="${changes_url}">
    <img src="/static/img/loading.gif" alt="Loading...">
</div>
