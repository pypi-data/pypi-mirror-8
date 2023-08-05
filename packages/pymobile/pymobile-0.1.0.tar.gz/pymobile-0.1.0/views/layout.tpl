<!DOCTYPE html> 
<html>
<head>
        <title>{{title}}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="/jqm142/css/jquery.mobile-1.4.2.min.css" />
        <script src="/jqm142/js/jquery-1.11.1.min.js"></script>
        <link rel="stylesheet" href="/jqm142/css/jquery.mobile.theme-1.4.2.min.css">
        <link rel="stylesheet" href="/jqm142/css/jquery.mobile.structure-1.4.2.min.css">
        
        <script src="/wsfunc.js"></script>
        <script type="text/javascript">
            $(document).bind("mobileinit", function() {
                //$.mobile.ajaxEnabled = false;
                $(document).on("pagecontainerloadfailed",function(event,data){
                    if (data.errorThrown == "Unauthorized" || data.errorThrown == "Forbidden") {
                        event.preventDefault();
                        location.href = "/login";
                    }
                });
            });
            $(document).ready( function() {
                 {{!documentready}}
            });
        </script>
        
        <script src="/jqm142/js/jquery.mobile-1.4.2.min.js"></script>
</head>

<body>
        %include
</body>
</html>