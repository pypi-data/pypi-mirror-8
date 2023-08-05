<table data-role="table" id="devicetable" data-mode="columntoggle" class="ui-body-d ui-shadow table-stripe ui-responsive" data-column-btn-theme="b" data-column-btn-text="Velg kolonne ..." data-column-popup-theme="a">
    <thead>
    <tr class="ui-bar-d">
        <th data-priority="1">Navn</th>
        <th data-priority="5">IP</th>
        <th data-priority="4"><abbr title="Kommando">Kommando</abbr></th>
        <th data-priority="3"><abbr title="Status">Status</abbr></th>
        <th data-priority="2">Send kommando:</th>
    </tr>
    </thead>
    <tbody>
    %for device in devices:
        <tr dev="{{device.ip}}">
            <th><p>{{device.name}}</p></th>
            <td><p>{{device.ip}}</p></td>
            <td>
            %if device.start:
                <p style="color:#00AA00;">Start</p>
            %elif device.stop:
                <p style="color:#AA0000;">Stop</p>
            %else:
                <p>Ingen</p>
            %end
            
            </td>
            <td>
            %if device.up:
                <p style="color:#00AA00;">Tilgjengelig</p>
            %elif device.down:
                <p style="color:#AA0000;">Ikke tilgjengelig</p>
            %else:
                    <p>Ukjent</p>
            %end
            </td>
            <td>
                <div data-role="controlgroup" data-type="horizontal" data-theme="e">
                <a href="/wol/{{device.mac}}" data-role="button" data-rel="dialog">Start</a>
                <a href="/shutdown/{{device.ip}}" data-role="button" data-rel="dialog">Stopp</a>
            </div>
            </td>
        </tr>
    %end
    </tbody>
</table>

<a href="/wol" data-role="button" data-ajax="false">Oppdater tabell</a>

<pre id="livedata">
    
     %for device in devices:
        l = $('tr[dev="{{device.ip}}"]>td>p');
        l.eq(1).text("{{device.start}} / {{device.stop}}");
        l.eq(2).text("{{device.up}} / {{device.down}}");
     %end
     
</pre>

<p id="counter">0</p>

<script type="text/javascript">
    i = 0;
    $(document).ready(function(){
        setInterval(function(){
        i += 1;
            $("#counter").text(i);
            $.get('/wol', function(data) {
                $("#livedata").text($("<div>").append(data).find('#livedata').html());
            });
        },2000);

    });
</script>

%rebase page title='WOL', pageid='wollist'
