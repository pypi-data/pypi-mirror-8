    <p>You are logged in as {{user}}</p>
    
    <a href="/" data-role="button" data-icon="home">Hjem</a>
    %include globalmenu
    
    <form method="POST" action="login">
        <hidden type="text" name="username" id="username" />
        <hidden type="password" name="password" id="password" value="" />
        <input type="submit" value="Logout" data-icon="grid" />
    </form>

%rebase page title=user, pageid='logout'

