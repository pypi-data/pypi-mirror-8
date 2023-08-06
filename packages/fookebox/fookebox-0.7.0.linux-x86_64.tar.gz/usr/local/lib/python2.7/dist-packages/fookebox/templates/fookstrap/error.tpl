<!DOCTYPE html>

<html lang="en">
	<head>
		<title>fookebox: ${ error }</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<link rel="stylesheet" href="/css/bootstrap/bootstrap.min.css" />
		<script src="/js/jquery/jquery-1.11.1.min.js"></script>
		<script src="/js/bootstrap/bootstrap.min.js"></script>
	</head>
	<body>
		<div class="navbar navbar-inverse navbar-fixed-top" role="navigation"></div>
		<div class="container">
			<div class="row">
				<div class="alert alert-danger" style="margin-top: 60px">
					${_('Error')}: ${ error }
				</div>
			</div>
		</div>
	</body>
</html>
