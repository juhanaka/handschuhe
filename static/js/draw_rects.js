$(function() {
    var coordinates_string = $('#coordinates').text();
    var coordinates = coordinates_string != '' ? $.parseJSON(coordinates_string) : null;
    var img_size_string = $('#img_size').text();
    var img_size = img_size_string != '' ? $.parseJSON(img_size_string) : null;
    var nLandmarkFeaturesStr = $('#n_landmark').text();
    var nLandmarkFeatures = nLandmarkFeaturesStr != '' ? $.parseJSON(nLandmarkFeaturesStr) : null;

    var general_opts = {trueSize: img_size, keySupport:false};

    _.each(_.keys(coordinates), function(coord) {
        if (coord.startsWith('landmark')) {
            $('#'+coord).annotatableImage(createBlackBox, {xPosition: 'middle', yPosition: 'middle'});
            $('#'+coord).mouseup(createAnnotationCallback(coord));
            $('#'+coord+'-clear').click(createClearAnnotationCallback(coord));
            if (coordinates[coord] == null) {
                return;
            }
            var coordinateArray = coordinates[coord];
            var coordinatesInFormat = [];
            for (var i=0; i < coordinateArray.length; i += 2) {
                coordinatesInFormat.push({x: coordinateArray[i]/(2*img_size[0]),
                                          y: coordinateArray[i+1]/img_size[1]});
            }
            if (coordinatesInFormat.length) {
                $('#'+coord).addAnnotations(createBlackBox, coordinatesInFormat);
            }
            return;
        }
        var opts = _.clone(general_opts);
        if (coordinates[coord] !== null) {
            opts.setSelect = coordinates[coord];
        }
        opts.onChange = generateJcropCallback(coord);
        opts.onSelect = generateJcropCallback(coord);
        $('#'+coord).Jcrop(opts);
    });

    function createBlackBox(coordinate) {
        return $(document.createElement('span')).addClass('black circle note');
    }

    function createAnnotationCallback(coordinate) {
        return function() {
            var serializedPositions = $('#' +coordinate + ' span.note').seralizeAnnotations();
            var formattedPositions = _.map(serializedPositions, function(obj) {
                console.log(obj)
                return (2*obj.x * img_size[0]).toString() + ','+ (obj.y *img_size[1]).toString();
            });
            $('#'+coordinate+'_xy').val(formattedPositions.join());
        }
    }
    function createClearAnnotationCallback(coordinate) {
        return function() {
            $('#'+coordinate+'_xy').val('');
            $('#'+coordinate+' span.note').remove();
        }
    }

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
        var notEnoughLandmarkFeatures = false;
        formData.forEach(function(el) {
            if (el.value == '') {
                isEmpty = true;
            }
            if (el.name.startsWith('landmark')) {
                if (el.value.split(',').length != (nLandmarkFeatures * 2)) {
                    notEnoughLandmarkFeatures = true;
                }
            }
        });
        if (isEmpty == true) {
            alert('You must select the bounding boxes!');
            ev.preventDefault();
        }
        else if (notEnoughLandmarkFeatures == true) {
            alert('You must pick ' + nLandmarkFeatures.toString() + ' landmark features!');
            ev.preventDefault();
        }
    });
});
