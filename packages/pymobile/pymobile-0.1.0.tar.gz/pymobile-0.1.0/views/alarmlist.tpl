<script>
    
    var ws = wsfunc('update_alarmlist', [], {}, function(evt) {
    
        data = JSON.parse(evt.data);
        $.each(data, function(i, al) {
            if (al.table == 'update') {
                var line = $("#"+al.id);
                $("th > p",line).text(al.s_time);
                var state = $("td:last > p",line);
                $(state).text(al.s_state);
                $(state).css("color", al.s_state_color);
            }
            else if (al.table == 'add') {
                $("#alarmtable > tbody").prepend(
                "<tr id='"+al.id+"'><th><p>"+al.s_time+
                "</p></th><td><p>"+al.desc+
                "</p></td><td><p onClick=\"ack_alarm('"+al.dpe+"');\" style='color:"+al.s_state_color+";'>"+al.s_state+"</p></td></tr>");
            }
            else if (al.table == 'remove') {
                $("#"+al.id).remove();
            }
        });
    });
    
    function ack_alarm(dpe) {
        if(confirm('acknowledge alarm?')) {
            ws.send(JSON.stringify(['ack_alarm', [], {'dpe':dpe}]));
        }
    }
    
</script>

<table
        data-role="table"
        id="alarmtable"
        data-mode="columntoggle"
        class="ui-body-d ui-shadow table-stripe ui-responsive"
        data-column-btn-theme="b"
        data-column-btn-text="Velg kolonne ..."
        data-column-popup-theme="a">
    <thead>
    <tr class="ui-bar-d">
        <th data-priority="3">Tid</th>
        <th data-priority="1"><abbr title="Beskrivelse">Beskrivelse</abbr></th>
        <th data-priority="2"><abbr title="Status">Status</abbr></th>
    </tr>
    </thead>
    <tbody>
    %for alarm in alarms:
        <tr id="{{alarm.id}}">
            <th><p>{{alarm.s_time}}</p></th>
            <td><p>{{alarm.desc}}</p></td>
            <td><p onClick="ack_alarm('{{alarm.dpe}}');" style="color:{{alarm.s_state_color}};">{{alarm.s_state}}</p></td>
        </tr>
    %end
    </tbody>
</table>

<a href="/alarmlist" data-role="button" data-ajax="false">Oppdater tabell</a>


%rebase page title='Alarmliste', pageid='alarmlist'
