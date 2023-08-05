<!DOCTYPE html> 
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1"> 
    <title>{{title}}</title> 
    <link rel="stylesheet" href="css/libs/jquery.mobile-1.1.0.min.css" />
    <script src="js/libs/jquery-1.7.2.min.js"></script>
    <script>
            $(document).bind("mobileinit", function(){
              $.mobile.ajaxEnabled = false;
               $.mobile.page.prototype.options.addBackBtn = true;
               $.mobile.page.prototype.options.backBtnText = "Tilbake";
            });
    </script>
    <script src="js/libs/jquery.mobile-1.1.0.min.js"></script>
    <style>
            .artikkel p{
                margin-top:0px;
                padding-top:0px;
            }
            
            .artikkel a:hover{
                text-decoration: underline;
            }
            
            .artikkel a{
                color: #153da4;
                text-decoration: none;
                font-weight: bold;
            }
            
            .artikkel #artikkelOverskrift{
                font-size: x-large;
                font-weight: bold;
            }
            
            .artikkel #artikkelDetaljer{
                color:#aaa;
                font-size: x-small;
            }

            .artikkel hr{
                border: 0px; 
                background-color: #aaa;
                color: #aaa;
                height: 1px;
                margin: 5px 0;
                padding: 0px;
            }
    </style>
</head> 

<body> 

<!-- Start of first page: #one -->
<div data-role="page" id="one">

    <div data-role="header" data-position="fixed">
    <a data-rel="back" data-icon="back" data-iconpos="notext">Tilbake</a>
        <h1>Multi-page</h1>
    </div><!-- /header -->

    <div data-role="navbar" data-iconpos="left">
        <ul>
        {{!"\n".join(['<li><a data-icon="star" href="%s">%s</a></li>' % (l,n) for n,l in nav.iteritems()])}}
        </ul>
    </div><!-- /navbar -->

    <div data-role="content">

    <ul data-role="listview" data-inset="true" data-icon="star">
        <li>Sidemeny
            <ul data-role="listview" data-inset="true" data-icon="star">
                <li data-role="list-divider">Sidemeny</li>
                <li><h3>Admin:</h3></li>
                <li><a href='admin_brukere.php'>   Brukere  </a></li>
                <li><a href='admin_bedrifter.php'> Bedrifter </a></li>
                <li><a href='admin_grupper.php'> Grupper </a></li>
                <li><a href='admin_dokumenter.php'> Dokumenter </a></li>
                <li><h3>User:</h3></li>
                <li><a href='bruker_detaljer.php'>Profil</a></li>
                <li><a href='artikkel_liste.php'>Mine artikler</a></li>
                <li><a href='bruker_logut.php'>Logg ut!</a></li>
            </ul>
        </li>
    </ul>

    <h2>One</h2>

    {{!content}}

    <h3>Show internal pages:</h3>
    <p><a href="#two" data-role="button">Show page "two"</a></p>	
    <p><a href="#popup"data-role="button" data-rel="dialog" data-transition="pop">Show page "popup" (as a dialog)</a></p>


    <ul>
    {{!"\n".join(['<h3>%s</h3><p>%s</p>\n' % (h,t) for h,t in aside.iteritems()])}}
    </ul>

    </div><!-- /content -->

    <div data-role="footer" data-position="fixed">
        <h4>{{footer}}</h4>
    </div><!-- /footer -->
    </div><!-- /page one -->


<!-- Start of second page: #two -->
<div data-role="page" id="two" data-theme="a">

	<div data-role="header">
		<h1>Two</h1>
	</div><!-- /header -->

	<div data-role="content" data-theme="a">	
		<h2>Two</h2>
		<p>I have an id of "two" on my page container. I'm the second page container in this multi-page template.</p>	
		<p>Notice that the theme is different for this page because we've added a few <code>data-theme</code> swatch assigments here to show off how flexible it is. You can add any content or widget to these pages, but we're keeping these simple.</p>	
		<p><a href="#one" data-direction="reverse" data-role="button" data-theme="b">Back to page "one"</a></p>	
		
	</div><!-- /content -->
	
	<div data-role="footer">
		<h4>Page Footer</h4>
	</div><!-- /footer -->
</div><!-- /page two -->


<!-- Start of third page: #popup -->
<div data-role="page" id="popup">

	<div data-role="header" data-theme="e">
		<h1>Dialog</h1>
	</div><!-- /header -->

	<div data-role="content" data-theme="d">	
		<h2>Popup</h2>
		<p>I have an id of "popup" on my page container and only look like a dialog because the link to me had a <code>data-rel="dialog"</code> attribute which gives me this inset look and a <code>data-transition="pop"</code> attribute to change the transition to pop. Without this, I'd be styled as a normal page.</p>		
		<p><a href="#one" data-rel="back" data-role="button" data-inline="true" data-icon="back">Back to page "one"</a></p>	
	</div><!-- /content -->
	
	<div data-role="footer">
		<h4>Page Footer</h4>
	</div><!-- /footer -->
</div><!-- /page popup -->

</body>
</html>
