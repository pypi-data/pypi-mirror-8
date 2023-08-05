Mako Sugar
===

A preprocessor that adds some syntactic sugar to Mako templates.

Write:

    % call foo():
        hi
    % endcall
        
instead of:

    <%call expr="foo()">
        hi
    </%call>
    
Install with:

        from mako_sugar import sugar
        
        # Any one of these options...
        t = Template(..., preprocessor=sugar())
        t = Template(..., preprocess=sugar(exclude=['def', 'call', 'import']))
        TemplateLookup(preprocessor=sugar())