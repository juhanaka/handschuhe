$(function() {
    var coordinates_string = $('#coordinates').text();
    console.log(coordinates_string);
    var coordinates = coordinates_string != '' ? $.parseJSON(coordinates_string) : null;
    var img_size_string = $('#img_size').text();
    var img_size = $.parseJSON(img_size_string);

    var general_opts = {trueSize: img_size, keySupport:false};

    _.each(_.keys(coordinates), function(coord) {
        var opts = _.clone(general_opts);
        if (coordinates.coord !== null) {
            console.log(coordinates[coord])
            opts.setSelect = coordinates[coord];
        }
        opts.onChange = generateJcropCallback(coord);
        opts.onSelect = generateJcropCallback(coord);
        $('#'+coord).Jcrop(opts);
    });

    function generateJcropCallback(coordinate) {
        return function(c) {
            $('#'+coordinate+'_ul_x').val(c.x);
            $('#'+coordinate+'_ul_y').val(c.y);
            $('#'+coordinate+'_lr_x').val(c.x2);
            $('#'+coordinate+'_lr_y').val(c.y2);
        };
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
    });
});
