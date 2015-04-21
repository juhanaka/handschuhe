$(function() {
    var coordinates_string = $('#coordinates').text()
    var coordinates = coordinates_string != '' ? $.parseJSON(coordinates_string) : null;
    var regular_opts = {onChange: showCoords, onSelect: showCoords};
    var left_opts = {onChange: showLCoords, onSelect: showLCoords};
    var right_opts = {onChange: showRCoords, onSelect: showRCoords};

    if (coordinates !== null) {
        regular_opts.setSelect = coordinates;
        left_opts.setSelect = coordinates.slice(0,4);
        right_opts.setSelect = coordinates.slice(4,8);
    }

    $('#labeled_image').Jcrop(regular_opts);
    $('#l_labeled_image').Jcrop(left_opts);
    $('#r_labeled_image').Jcrop(right_opts);


    function showCoords(c) {
        $('#x').val(c.x);
        $('#y').val(c.y);
        $('#x2').val(c.x2);
        $('#y2').val(c.y2);
    }

    function showLCoords(c) {
        $('#l_x').val(c.x);
        $('#l_y').val(c.y);
        $('#l_x2').val(c.x2);
        $('#l_y2').val(c.y2);
    }

    function showRCoords(c) {
        $('#r_x').val(c.x);
        $('#r_y').val(c.y);
        $('#r_x2').val(c.x2);
        $('#r_y2').val(c.y2);
    }
});
