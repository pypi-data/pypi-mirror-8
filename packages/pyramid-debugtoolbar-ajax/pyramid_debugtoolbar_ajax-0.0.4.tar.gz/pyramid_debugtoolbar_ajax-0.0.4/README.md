pyramid_debugtoolbar_ajax
=========================

This adds an "Ajax" panel to the pyramid_debugtoolbar

This panel contains a button to replay the request in a new window -- allowing you to spawn a debugger window for errors encountered on background ajax requests.

How to use:

Add this to your pyramid includes:

    pyramid.includes = pyramid_debugtoolbar pyramid_debugtoolbar_ajax
