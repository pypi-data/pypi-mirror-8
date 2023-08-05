
    <ul data-role="listview" data-autodividers="true" id="sortedList">
    %for id, album in albumer.items():
        <li><a href="/sang/{{id}}">{{album}}</a></li>
    %end
    </ul><!-- /listview -->

%rebase page title='Albumliste', pageid='albumliste'

