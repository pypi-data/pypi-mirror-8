<%inherit file="base.tpl"/>

<%def name="headers()">
	<script type="text/javascript" src="js/fookebox/classic/client.js"></script>
</%def>

<div id="message" style="display: none">
	<div class="corner tl"></div>
	<div class="corner tr"></div>
	<div class="corner bl"></div>
	<div class="corner br"></div>
	<div id="messageText"></div>
</div>
<h1 id="h1"><a href="/">${config.get('site_name')}</a></h1>
<%include file="browse-menu.tpl"/>
<div id="status">
<%include file="status.tpl"/>
</div>
<img src="img/classic/progress.gif" alt="" id="progress" style="display: none" />
<div id="searchResult"></div>
