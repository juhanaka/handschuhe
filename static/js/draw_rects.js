$(function() {
    var coordinates_string = $('#coordinates').text();
    var coordinates = coordinates_string != '' ? $.parseJSON(coordinates_string) : null;
    var img_size_string = $('#img_size').text();
    var img_size = img_size_string != '' ? $.parseJSON(img_size_string) : null;
    var nLandmarkFeaturesStr = $('#n_landmark').text();
    var nLandmarkFeatures = nLandmarkFeaturesStr != '' ? $.parseJSON(nLandmarkFeaturesStr) : null;

    var general_opts = {trueSize: img_size, keySupport:false, bgColor: 'white', bgOpacity: 0.3};
    var landmark_idx = 1;

    if (typeof String.prototype.startsWith != 'function') {
        // see below for better implementation!
        String.prototype.startsWith = function (str){
            return this.indexOf(str) === 0;
        };
    }

    _.each(_.keys(coordinates), function(coord) {
        if (coord.startsWith('landmark')) {
            $('#'+coord).annotatableImage(createBlackBox, {xPosition: 'middle', yPosition: 'middle'});
            $('#'+coord).mouseup(createAnnotationCallback(coord));
            $('#'+coord+'-clear').click(createClearAnnotationCallback(coord));
            $('#'+coord+'-undo').click(createUndoAnnotationCallback(coord));
            if (coordinates[coord] == null) {
                return;
            }
            var coordinateArray = coordinates[coord];
            var coordinatesInFormat = [];
            for (var i=0; i < coordinateArray.length; i += 2) {
                coordinatesInFormat.push({x: coordinateArray[i]/(img_size[0]),
                                          y: coordinateArray[i+1]/img_size[1]});
            }
            if (coordinatesInFormat.length) {
                console.log(coordinatesInFormat);
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
        var el = $(document.createElement('span'))
            .addClass('red dot note')
            .attr('id', 'landmark-'+landmark_idx.toString())
            .text("\n"+landmark_idx);
        landmark_idx++;
        return el;
    }

    function createAnnotationCallback(coordinate) {
        return function() {
            var serializedPositions = $('#' +coordinate + ' span.note').seralizeAnnotations();
            var formattedPositions = _.map(serializedPositions, function(obj) {
                return (obj.x * img_size[0]).toString() + ','+ (obj.y *img_size[1]).toString();
            });
            $('#'+coordinate+'_xy').val(formattedPositions.join());
        }
    }
    function createClearAnnotationCallback(coordinate) {
        return function() {
            $('#'+coordinate+'_xy').val('');
            $('#'+coordinate+' span.note').remove();
            landmark_idx = 1;
        }
    }
    function createUndoAnnotationCallback(coordinate) {
        return function() {
            var notes = $('#'+coordinate+' span.note');
            _.max(notes, function(note) {
                return parseInt($(note).attr('id').split('-')[1]);
            }).remove();
            var coordStr = $('#'+coordinate+'_xy').val();
            var newCoordStr = coordStr.split(',').slice(0,-2).join(',');
            $('#'+coordinate+'_xy').val(newCoordStr);
            landmark_idx--;
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
                console.log(el);
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
