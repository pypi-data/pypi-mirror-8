% setdefault('pageid', 'defaultdialog')
% setdefault('documentready', 'documentready')
% setdefault('title', 'dialog')
% setdefault('okbutton', False)

<div data-role="page" id="{{pageid}}">

    <div data-role="header">
        <h1>{{title}}</h1>
    </div>
        
    <div data-role="content">
    
        {{!content}}
        
        %if okbutton:
            <a href="#" data-rel="back" data-icon="arrow-l" data-role="button" data-ajax="false">OK</a>
        %end

    </div>
    
</div>

%rebase layout title=title, documentready=documentready
