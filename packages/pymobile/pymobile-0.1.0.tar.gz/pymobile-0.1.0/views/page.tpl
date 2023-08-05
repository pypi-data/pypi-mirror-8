% setdefault('pageid', 'page1')
% setdefault('documentready', '//documentready')
% setdefault('title', 'dialog')
% setdefault('content', '')

<div data-role="page" id="{{pageid}}">

    <div data-role="panel" id="mypanelmenu">
        <a href="/" data-role="button" data-icon="home">Hjem</a>
        %include globalmenu
        <a href="#startpage" data-role="button" data-rel="close" data-icon="delete">Lukk</a>
    </div>

    <div data-role="header">
        <h1>{{title}}</h1>
        <a href="#mypanelmenu" data-role="button" data-inline="true" data-icon="bars" data-iconpos="notext">Menu</a>
    </div>
        
    <div role="main" class="ui-content">
        %if content:
            {{!content}}
        %else:
            %include
        %end

    </div>
    
</div>

%rebase layout title=title, documentready=documentready
