    <p>{{message}}</p>
    <form method="POST" action="login">
            <label for="username">Name:</label>
            <input type="text" name="username" id="username"/>
            
            <label for="password">Password:</label>
            <input type="password" name="password" id="password" value=""/>

            <input type="submit" value="Submit" data-icon="grid" data-iconpos="right" />
        </form>

%rebase page title='Login', pageid='login'

