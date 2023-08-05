
    <ul data-role="listview" data-autodividers="true" id="sortedList">
    %for id, artist in artister.items():
        <li><a href="/album/{{id}}?mappe={{artist}}">{{artist}}</a></li>
    %end
    </ul><!-- /listview -->
            
%rebase page title='Artistliste', pageid='artistliste'

