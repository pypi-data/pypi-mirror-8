    
    <p>
        <ul>
            <li>sid: {{session.sid}}</li>
        %for k, v in session.items():
            <li>{{k}}: {{v}}</li>
        %end
        </ul>
    </p>
    
    <form method="POST" action="/session">
        <label for="test1">Test 1:</label>
        <input type="text" name="test1" id="test1" value="{{session.get('test1','')}}" />
        
        <label for="test2">Test 2:</label>
        <input type="text" name="test2" id="test2" value="{{session.get('test2','')}}" />

        <label for="test3">Test 3:</label>
        <input type="text" name="test3" id="test3" value="{{session.get('test3','')}}" />
        
        <label for="test4">Test 4:</label>
        <input type="text" name="test4" id="test4" value="{{session.get('test4','')}}" />
        
        <input type="submit" value="Submit" data-icon="grid" data-iconpos="right" />
    </form>

%rebase page title='Session test', pageid='sessiontest'

