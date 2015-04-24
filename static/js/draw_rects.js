$(function() {
    var coordinates_string = $('#coordinates').text();
    var coordinates = coordinates_string != '' ? $.parseJSON(coordinates_string) : null;
    var img_size_string = $('#img_size').text();
    var img_size = $.parseJSON(img_size_string);
    var regular_opts = {onChange: showCoords, onSelect: showCoords, trueSize: img_size, boxWidth: 600, boxHeight: 600};
    var left_opts = {onChange: showLCoords, onSelect: showLCoords, trueSize: img_size,};
    var right_opts = {onChange: showRCoords, onSelect: showRCoords, trueSize: img_size,};

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
    $(window).keyup(function(ev) {
        if (ev.which == 13) {
            $('.hidden_form').submit();
        } else if (ev.which == 37) {
            if ($('#prev').length) {
                $('#prev')[0].click();
            }
        } else if (ev.which == 39) {
            if ($('#next').length) {
                $('#next')[0].click();
            }
        }
    });
    $('.hidden_form').submit(function(ev) {
        var formData = $('.hidden_form').serializeArray();
        var isEmpty = false;
        formData.forEach(function(el) {
            if (el.value == '') {
                isEmpty = true;
            }
        });
        if (isEmpty == true) {
            alert('You must select the bounding boxes!');
            ev.preventDefault();
        }
    })
});
