<script>
    
    var live = wsfunc('livecounter', [], {}, function(evt) {
        $('#count').text(JSON.parse(evt.data));
    });
    
</script>
    
    <p>Eksempel på visning av artister: <a href='/artister'>Artister</a></p>

    <p>Eksempel innlogging: <a href='/login' data-ajax="false">Login</a>,  <a href='/restricted'>Restricted page</a></p>
    
    <p>Eksempel session: <a href='/session'>session</a></p>

    <p>Alarmlist: <a href='/alarmlist/'>Alarmlist</a></p>
    
    <p>Livecounter: <span id="count">{{livecounter}}</span> </p>

    <p>Eksempel på WOL: <a href='/wol'>WOL</a></p>

    <p>Debug-data: <a href='/debug'>Debug</a></p>

%rebase page title='Startside', pageid='startpage'

