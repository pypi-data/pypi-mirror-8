<%inherit file="base.tpl"/>
<h1 id="h1"><a href="/">${config.get('site_name')}</a></h1>
<div id="meta">
	<a href="https://github.com/cockroach/fookebox">fookebox</a> ${config.get('version')}<br />
	&copy; 2007-2014 <a href="http://www.ott.net/">Stefan Ott</a>
</div>
<div style="font-size: large; text-align: center; margin-top: 200px">
${_('Error')}: ${ error }
</div>
