function id_to_windowname(text) {
    text = text.replace(/\./g, '__dot__');
    text = text.replace(/\-/g, '__dash__');
    return text;
}

function windowname_to_id(text) {
    text = text.replace(/__dot__/g, '.');
    text = text.replace(/__dash__/g, '-');
    return text;
}

function showMediaObjectLookupPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^lookup_/, '');
    name = id_to_windowname(name);
    var href;
    if (triggeringLink.href.search(/\?/) >= 0) {
        href = triggeringLink.href + '&pop=1';
    } else {
        href = triggeringLink.href + '?pop=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

var django_dismissAddAnathorPopup = dismissAddAnotherPopup;
function dismissAddAnotherPopup(win, newId, newRepr) {
    // newId and newRepr are expected to have previously been escaped by
    // django.utils.html.escape.
    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem) {
        if (elem.nodeName == 'SELECT') {
            var o = new Option(newRepr, newId);
            elem.options[elem.options.length] = o;
            o.selected = true;
        } else if (elem.nodeName == 'INPUT') {
            if ($(elem).hasClass('vManyToManyRawIdAdminField') && elem.value) {
                elem.value += ',' + newId;
                getMediaPreviews(name, newId, true);
            } else {
                elem.value = newId;
                getMediaPreviews(name, newId);
            }
        }
    } else {
        var toId = name + "_to";
        elem = document.getElementById(toId);
        var o = new Option(newRepr, newId);
        SelectBox.add_to_cache(toId, o);
        SelectBox.redisplay(toId);
    }
    win.close();
}

function deleteMediaRelation(field_name, field_id, media_id) {
    var value = jQuery('#' + field_id).attr('value'),
        newvalue = [];
    value = value.split(',');
    for (var i = 0; i < value.length; i++) {
        if (value[i] != media_id) {
            newvalue.push(value[i]);
        }
    }
    jQuery('#' + field_id).attr('value', newvalue.join(','));
    jQuery('.preview-' + field_name + '-' + media_id).remove();
}

function mediaSelectAPI(name, params, callback) {
    var apiurl = jQuery('#' + name).siblings('a.related-lookup').attr('href');
    apiurl = apiurl.split('?')[0];
    jQuery.getJSON(apiurl, params, callback);
}

function getMediaPreviews(name, ids, append) {
    mediaSelectAPI(name, {_get_previews: ids}, function (data) {
        if (!append) {
            jQuery('#' + name).siblings('.previews').empty();
        }
        jQuery.each(data, function () {
            var id = parseInt(this.id),
                preview = this.preview;
            preview = jQuery(preview);
            preview.append(
                '<a href="javascript:deleteMediaRelation(' + 
                    '\'' + name.replace(/^id_/,'') + '\', \'' + name + '\', \'' + id + '\'' +
                ');" class="deletelink-media"></a>');
            jQuery('#' + name).siblings('.previews').append(preview);
        });
    });
};

(function ($) {
    $(document).ready(function () {
        var selected_media = [],
            name, elem, opts;

        function dismissMediaObjectLookupPopup(win, chosenId) {
            if (elem.hasClass('vManyToManyRawIdAdminField')) {
                if (chosenId === null) {
                    elem.val(selected_media.join(','));
                } else {
                    if (elem.val()) {
                        elem.val(elem.val() + ',');
                    }
                    elem.val(elem.val() + chosenId);
                }
            } else {
                elem.val(chosenId);
            }
            opts.select_cache = undefined;
            opener.getMediaPreviews(name, elem.val());
            win.close();
            return false;
        }

        function addSelectedMedia(id) {
            selected_media.push(id);
            opts.select_cache = selected_media;
            updateSelectedFilter();
        }

        function removeSelectedMedia(id) {
            var remove_index = [];
            $.each(selected_media, function (i) {
                if (this == id) {
                    remove_index.push(i);
                }
            });
            $.each(remove_index, function (i) {
                selected_media.splice(this-i, 1);
            });
            opts.select_cache = selected_media;
            updateSelectedFilter();
        }

        function updateSelectedFilter() {
            $('a[href*=pk__in=]').each(function () {
                var bits = $(this).attr('href').split('?');
                    bits2 = bits[1].split('&');
                $.each(bits2, function (i) {
                    if (this.match(/^pk__in=/)) {
                        bits2[i] = 'pk__in=' + selected_media.join(',');
                    }
                });
                $(this).attr('href', bits[0] + '?' + bits2.join('&'));

            });
        }

        if (window.MEDIASELECT_POPUP !== undefined) {
            name = windowname_to_id(window.name);
            elem = $(window.opener.document).find('#' + name);
            if (window.opener.MEDIASELECT[name] === undefined) {
                window.opener.MEDIASELECT[name] = {};
            }
            opts = window.opener.MEDIASELECT[name];
            if (elem.hasClass('vManyToManyRawIdAdminField')) {
                if (elem.val() != '') {
                    selected_media = elem.val().split(',');
                }
            }

            if (opts.select_cache === undefined) {
                opts.select_cache = selected_media;
            } else {
                selected_media = opts.select_cache;
            }

            updateSelectedFilter();

            $.each(selected_media, function () {
                $('#media-id-' + this).addClass('selected');
            });
        } else {
            if (window.MEDIASELECT === undefined) {
                window.MEDIASELECT = {};
            }
            var previews = $('.vManyToManyRawIdAdminField.sorted').siblings('.previews');
            previews.sortable({
                containment: 'parent',
                items: '.preview',
                update: function (event, ui) {
                    var newids = [];
                    $(this).find('.preview').each(function () {
                        newids.push($(this).attr('class').match(/preview-.+-(\d+)/)[1]);
                    });
                    $(this).siblings('.vManyToManyRawIdAdminField').val(newids.join(','));
                }
            });
        }

        $('#media-list.select-single .media-object').click(function () {
            var media_id = this.id.match(/media-id-(\d+)/)[1];
            return dismissMediaObjectLookupPopup(window, media_id);
        });
        $('#media-list.select-multiple .media-object').click(function () {
            var id = this.id.match(/media-id-(\d+)/)[1];
            if ($(this).hasClass('selected')) {
                removeSelectedMedia(id);
                $(this).removeClass('selected');
            } else {
                addSelectedMedia(id);
                $(this).addClass('selected');
            }
        });

        function mediaObjectMatch(obj) {
            var searchterm = $('#searchbar').attr('value'),
                type, select = $('*[id^=show-mediatype-].selected');

            if (searchterm) {
                if (obj.find('.meta.keywords').text().toLowerCase().indexOf(searchterm.toLowerCase()) === -1) {
                    return false;
                }
            }
            if (select.length) {
                type = select.attr('id').match(/show-mediatype-(.*)/)[1];
            }
            if (type && type != '-all') {
                if (type == '-selected') {
                    type = 'selected';
                } 
                if (!obj.hasClass(type)) {
                    return false;
                }
            }
            return true;
        }

        function showMediaObjects() {
            $('.media-object').each(function (i) {
                var obj = $(this);
                if (mediaObjectMatch(obj)) {
                    obj.show();
                } else {
                    obj.hide();
                }
            });
        }

        $('#searchbar').change(showMediaObjects).keyup(showMediaObjects);
        $('*[id^=show-mediatype-]').click(function () {
            var id = this.id.match(/show-mediatype-(\d+)/)[1];
            $(this).addClass('selected');
            $(this).siblings().removeClass('selected');
            showMediaObjects();
        });

        $('*[name=submit]').click(function () {
            dismissMediaObjectLookupPopup(window, null);
            return false;
        });
    });
})(jQuery);
