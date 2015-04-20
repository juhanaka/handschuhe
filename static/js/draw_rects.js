$(function() {
    $('#labeled_image').Jcrop({
        onChange: showCoords,
        onSelect: showCoords
    });
    function showCoords(c) {
        $('#x').val(c.x);
        $('#y').val(c.y);
        $('#x2').val(c.x2);
        $('#y2').val(c.y2);
    };
    $('#l_labeled_image').Jcrop({
        onChange: showLCoords,
        onSelect: showLCoords
    });
    function showLCoords(c) {
        $('#l_x').val(c.x);
        $('#l_y').val(c.y);
        $('#l_x2').val(c.x2);
        $('#l_y2').val(c.y2);
    };
    $('#r_labeled_image').Jcrop({
        onChange: showRCoords,
        onSelect: showRCoords
    });
    function showRCoords(c) {
        $('#r_x').val(c.x);
        $('#r_y').val(c.y);
        $('#r_x2').val(c.x2);
        $('#r_y2').val(c.y2);
    };
})
