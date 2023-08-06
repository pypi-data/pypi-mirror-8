/* Begin sloppy globals */
// http://stackoverflow.com/a/956878
function countProperties(obj) {
    var count = 0;

    for(var prop in obj) {
        if(obj.hasOwnProperty(prop))
            ++count;
    }

    return count;
}

// http://stackoverflow.com/a/646643/1991086
if (typeof String.prototype.startsWith != 'function') {
    String.prototype.startsWith = function (str){
        return this.slice(0, str.length) == str;
    };
}

var updateTimeout;
var topic_colors = {};
var activeTopics = [];
var tags_top_only = true;
var color_ramps = true;
var num_ramps = 5;
var rank_type = 'sal';
var color_set_name = "baseColors";
var page_index = -1;
var page_uris = [];
/* End sloppy globals */

// TODO: don't need anymore now that TextViewer.py is passing us rules variable
var getIncludedTopics = function() {
    x = [];
    d3.selectAll('.btn-label')
        .each(function() {
            x.push(d3.select(d3.select(this).node().parentNode).attr('data-key'));
        });
    return x;
};

// TODO: fix reference to 'data-key'
var updateTopicNames = function() {
    d3.json($GET_TOPIC_NAMES_URL, function(json) {
        if (json.topicNames != null){
            d3.selectAll('.btn-label')
                .text(function() {
                    var topicNum = parseInt(d3.select(d3.select(this).node().parentNode).attr('data-key').split('_')[1]);
                    return json.topicNames[topicNum];
                });
        }
    });
};

var storeTopicColors = function() {
    var storageStr = '';
    var i = 0;
    for (var topicID in topic_colors) {
        if (i != 0) {
            storageStr += ';'
        }
        storageStr += topicID + ':' + topic_colors[topicID];
        i++;
    }
    localStorage[corpus_name] = storageStr;
};

var retrieveAndApplyTopicColors = function(oldRankType) {
    var topicAssignments = localStorage[corpus_name].split(';');
    var colors = app_colors[color_set_name];
    var tempTopicColors = {};
    var tmp, topic_class_str, color, $btn;
    var colorSansPound, classToSelect, classToAdd, classToRemove;
    var rankTypeToRemove;
    for (var i = 0; i < topicAssignments.length; i++) {
        if (topicAssignments[i] != '') {
            tmp = topicAssignments[i].split(':');
            topic_class_str = tmp[0];
            color = tmp[1];
            tempTopicColors[topic_class_str] = color;

            $btn = $('#btn-' + topic_class_str);
            if (topic_class_str in topic_colors) {
                // Remove old color
                colorSansPound = topic_colors[topic_class_str].substring(1);
                $btn.removeClass('noramp_' + colorSansPound);
                for (var j = 1; j <= num_ramps; j++) {
                    if (oldRankType == undefined) {
                        rankTypeToRemove = rank_type;
                    } else {
                        rankTypeToRemove = oldRankType;
                    }
                    classToSelect = rankTypeToRemove + j + '.' + topic_class_str;
                    // Remove both noramp and ramped, not knowing whether color_ramps just changed
                    $('.' + classToSelect).removeClass(rankTypeToRemove + colorSansPound);
                    $('.' + classToSelect).removeClass('noramp_' + colorSansPound);
                }
            } else {
                $btn.addClass('active');
                activeTopics.push(topic_class_str);
            }
            // Add new color
            colorSansPound = color.substring(1);
            $btn.addClass('noramp_' + colorSansPound);
            for (var j = 1; j <= num_ramps; j++) {
                classToSelect = rank_type + j + '.' + topic_class_str;
                classToAdd = color_ramps ? rank_type + colorSansPound
                                         : 'noramp_' + colorSansPound;
                $('.' + classToSelect).toggleClass(classToAdd);
            }
        }
    }

    // Untoggle non-active topics
    for (var topic in topic_colors) {
        if (!(topic in tempTopicColors)) {
            colorSansPound = topic_colors[topic].substring(1);
            $('#btn-' + topic).removeClass("active")
                              .removeClass('noramp_' + colorSansPound);
            for (var j = 1; j <= num_ramps; j++) {
                classToSelect = rank_type + j + '.' + topic;
                classToRemove = color_ramps ? rank_type + colorSansPound
                                            : 'noramp_' + colorSansPound;
                $('.' + classToSelect).removeClass(classToRemove);
            }
            activeTopics.splice(activeTopics.indexOf(topic), 1);
        }
    }

    topic_colors = tempTopicColors;
    clearTimeout(updateTimeout);
    updateTimeout = setTimeout(
        updateLineGraph,
        100
    );
};

/* Code for tag buttons in sidebar */
var handleTagButtons = function(event) {
    var topic_class_str = $(this).attr("data-key");
    toggleTopic(topic_class_str);
};

var toggleTopic = function(topic_class_str) {
    var $btn = $('#btn-' + topic_class_str);
    if (! $btn.hasClass("active")) {
        $btn.addClass("active");
        activeTopics.push(topic_class_str);

        var colors = app_colors[color_set_name];
        var color_index = getNextUnusedColorIndex(colors, topic_colors);
        var colorSansPound = colors[color_index].substring(1);
        for (var j = 0; j < activeTopics.length; j++) {
            var class_str = activeTopics[j];
            if (! topic_colors.hasOwnProperty(class_str)) {
                topic_colors[class_str] = colors[color_index];
            }
        }
    }
    else {
        $btn.removeClass("active");
        // Free up this topic's color.
        var colorSansPound = topic_colors[topic_class_str].substring(1);
        delete topic_colors[topic_class_str];
        activeTopics.splice(activeTopics.indexOf(topic_class_str), 1);
    }

    // Apply colors (using hueRamps)
    $btn.toggleClass('noramp_' + colorSansPound);
    var classToSelect, classToToggle;
    for (var j = 1; j <= num_ramps; j++) {
        classToSelect = rank_type + j + '.' + topic_class_str;
        classToToggle = color_ramps ? rank_type + colorSansPound
                                 : 'noramp_' + colorSansPound;
        $('.' + classToSelect).toggleClass(classToToggle);
    }

    storeTopicColors();
    clearTimeout(updateTimeout);
    updateTimeout = setTimeout(
        updateLineGraph,
        100
    );
};

var getNextUnusedColorIndex = function(colors, topic_colors) {
    // The index to use when all other colors are used up.
    var index_to_return = colors.length - 1;
    for (var j = 0; j < colors.length - 1; j++) {
        var color = colors[j];
        if (countProperties(topic_colors) == 0) {
            index_to_return = j;
            break;
        }
        else {
            // Verify that this color is unused.
            var is_unused = true;
            for (var prop in topic_colors) {
                if (topic_colors.hasOwnProperty(prop) && color == topic_colors[prop]) {
                    is_unused = false;
                }
            }
            if (is_unused) {
                index_to_return = j;
                break;
            }
        }
    }
    return index_to_return;
};

var updateLineGraph = function() {
    // Generate CSS for topics based on the colors we assigned them.
    var css_str = "";
    for (var topic_key in topic_colors) {
        if (topic_colors.hasOwnProperty(topic_key)) {
            var topic_color = topic_colors[topic_key];
            /* LineGraphFormatter Styles */
            css_str += ".topic_model_line_graph g." + topic_key + " { opacity: 1.0; }\n";
            css_str += ".topic_model_line_graph g." + topic_key + " rect { fill-opacity: 0.0625; }\n";
            css_str += ".topic_model_line_graph g." + topic_key + ":hover rect { fill-opacity: 0.375; }\n";
            css_str += ".topic_model_line_graph g." + topic_key + " use.polyline { stroke: " + topic_color + "; }\n";
            /* Popover styles */
            css_str += ".popover rect[data-key~=" + topic_key + "] { fill: " + topic_color + "; }\n";
        }
    }
    // Insert the CSS into the DOM.
    var $css_el = $("<style class='topic_model' type='text/css'>");
    $css_el.text(css_str);
    if ($("style.topic_model").get(0)) {
        $("style.topic_model").replaceWith($css_el);
    }
    else {
        $("head").append($css_el);
    }
};

var fetchLineGraph = function(extraCallback) {
    $("#right_sidebar_content").addClass("withLoadingIndicator");
    // Generate the URI to the new line graph SVG.
    var pixel_size = $('#right_sidebar_content').height();
    var line_graph_uri = flask_util.url_for(
        "text_get_mallet_line_graph", {
            "corpus_name": corpus_name,
            "text_name": text_name,
            "ranking_type": rank_type
        }
    );
    // Fetch the new SVG DOM with jQuery and insert it into the DOM.
    var $old_el = $("#right_sidebar_content .topic_model_line_graph");
    $.get(line_graph_uri, function(response) {
        var $response = $(response);
        $("#right_sidebar_content").removeClass("withLoadingIndicator");
        $old_el.replaceWith($response);

        // Attach events.
        attachLineGraphEventsToElement($response);
        if (extraCallback != undefined) {
            extraCallback();
        }
    });
};

var attachLineGraphEventsToElement = function(el) {
    $("g[data-key]", el).on("click", function() {
        console.log(this);
        var $buttons_to_activate = $("#sidebar .btn-tag").filter("[data-key=" + $(this).attr("data-key") + "]");
        $buttons_to_activate.trigger("click");
    }).on("mouseover", function() {
        syncTopicBrushing($(this).attr("data-key"));
    }).on("mouseout", function() {
        endSyncTopicBrushing($(this).attr("data-key"));
    }).on("contextmenu", function() {
        var $buttons_to_activate = $("#sidebar .btn-tag").filter("[data-key=" + $(this).attr("data-key") + "]");
        $buttons_to_activate.trigger("contextmenu");
    });

    $(".page_locator", el).on("click", function(e) {
        e.preventDefault();
        // Get the range of tag maps this tag map locator represents.
        var tag_map_page_index = parseInt($(this).attr("data-page-index"));

        // We need to go to a different page if the first (or last) tag map is out of range of the current page.
        if (tag_map_page_index != page_index) {
            change_to_page(tag_map_page_index);
        }

        window.location.hash = $(this).attr('xlink:href');
    });
};

/* End code for tag buttons in sidebar */

/* Code for word distribution popovers */
var clearPopovers = function() {
    $("body .popover").remove();
    $("body .html_formatter > span.active").removeClass("active");
    clearPopoverEvents();
};

var getBottomPosition = function(popover_el) {
    // This only works correctly for pixel values!!!
    return (
        parseInt(
            $(popover_el).css("top")
        ) +
        $(popover_el).height() +
        parseInt(
            $(popover_el).css("padding-top")
        ) +
        parseInt(
            $(popover_el).css("padding-bottom")
        ) +
        parseInt(
            $(popover_el).css("border-top")
        ) +
        parseInt(
            $(popover_el).css("border-bottom")
        )
    );
};

var clearPopoverEvents = function() {
    $(window)
        .off("click.getTopicsForWordElement")
        .off("scroll.getTopicsForWordElement")
        .off("resize.getTopicsForWordElement")
        .off("keydown.getTopicsForWordElement");
};

var conditionallyClearPopovers = function(event) {
    var condition = ! (
        $(event.target).is("#main .html_formatter > span") ||
        $(event.target).parents("#main .html_formatter > span").length > 0
    );

    if (condition) {
        clearPopovers();
    }
};

var reshowActivePopovers = function(event) {
    var $active_spans = $(".html_formatter > span.active");
    $active_spans.popover('show');
};

var reshowActivePopoversWithTimeout = function(event) {
    clearTimeout(updateTimeout);
    updateTimeout = setTimeout(
        reshowActivePopovers,
        100
    );
};

var closePopoversWithEscKey = function(event) {
    // Look for keycode for Esc key
    if (event.keyCode == 27) {
        clearPopovers();
    }
};

var attachPopoverEvents = function(element) {
    $(element)
        .on("click.getTopicsForWordElement", conditionallyClearPopovers)
        .on("scroll.getTopicsForWordElement", reshowActivePopoversWithTimeout)
        .on("resize.getTopicsForWordElement", reshowActivePopoversWithTimeout)
        .on("keydown.getTopicsForWordElement", closePopoversWithEscKey);
};

// Events for .html_formatter tokens, etc.
var getTopicsForWordElement = function() {
    var word = $.trim($(this).text());
    // Open word in wordRankings
    window.open(flask_util.url_for('wordRankings',
        { corpus_name: corpus_name,
          rankingType: rank_type,
          wordColorPairs: word.toLowerCase() + ':red'
        }));

    // Do nothing if this "word" was either nothing or just whitespace.
    if (word === "") {
        return;
    }
    // Remove existing popovers.
    clearPopovers();
//    // Create the new popover right away.
//    var that = this;
//    var topic_dist_container_id = "topic_dist_" + $(this).attr("id");
//    $(this)
//        .addClass("active")
//        .popover({
//            title: "Topic Distributions for &ldquo;" + word + "&rdquo;",
//            html: true,
//            trigger: "manual",
//            placement: "bottom",
//            animation: false,
//            container: "body"
//        });
//        // .popover('show');
//    $(this).data("popover").options.content = "<div id='" + topic_dist_container_id + "' class='withLoadingIndicator' style='height: 84px'></div>";
//    $(this).popover("show");
//    /* Reposition the popover if it's tall enough to be off-screen. */
//    if (getBottomPosition($(this).data().popover.$tip) > $(window).height() - 12) {
//        $(this).data().popover.options.placement = "top";
//        $(this).popover("show");
//    } else {
//        $(this).data().popover.options.placement = "bottom";
//        $(this).popover("show");
//    }
//
//    // Generate the topic distribution.
//    genWordView(corpus_name, text_name, word, this);
//
//    // Attach events to close the popovers.
//    attachPopoverEvents(window);
};
/* end code for word distribution popovers */

/* Code for synced brushing */

var syncTopicBrushing = function(tag_key) {
    // Add ".highlight" to related elements.
    d3.selectAll(".topic_model_line_graph g[data-key='" + tag_key + "']")
        .classed("highlight", true);
    d3.selectAll("#sidebar .btn-tag[data-key='" + tag_key + "']")
        .classed("highlight", true);
    d3.selectAll(".popover rect.bar[data-key='" + tag_key + "']")
        .style("fill", "#ffff99");
    d3.selectAll(".html_formatter > span[data-key~='" + tag_key + "']")
        .classed("highlight", true);
};

var endSyncTopicBrushing = function(tag_key) {
    d3.selectAll(".topic_model_line_graph g[data-key='" + tag_key + "']")
        .classed("highlight", false);
    d3.selectAll("#sidebar .btn-tag[data-key='" + tag_key + "']")
        .classed("highlight", false);
    d3.selectAll(".popover rect.bar[data-key='" + tag_key + "']")
        .style("fill", false);
    d3.selectAll(".html_formatter > span[data-key~='" + tag_key + "']")
        .classed("highlight", false);
};

/* End code for synced brushing */

// Code for changing the text tagging display mode.
var changeTagDisplayMode = function(new_mode_value) {
    if (new_mode_value !== undefined) {
        tags_top_only = new_mode_value;
    }
    else {
        tags_top_only = ! tags_top_only;
    }
    if (tags_top_only) {
        $(".btn-group.color_ramps .btn").addClass("tags_top_only_on");
        $(".btn-group.tags_top_only .btn.btn-tags_top_only_on").addClass("btn-primary");
        $(".btn-group.tags_top_only .btn.btn-tags_top_only_off").removeClass("btn-primary");
    }
    else {
        $(".btn-group.color_ramps .btn").removeClass("tags_top_only_on");
        $(".btn-group.tags_top_only .btn.btn-tags_top_only_on").removeClass("btn-primary");
        $(".btn-group.tags_top_only .btn.btn-tags_top_only_off").addClass("btn-primary");
    }
    updateLineGraph();
};

var changeColorRampsMode = function(new_mode_value) {
    if (new_mode_value !== undefined) {
        color_ramps = new_mode_value;
    }
    else {
        color_ramps = ! color_ramps;
    }
    if (color_ramps) {
        $(".btn-group.tags_top_only .btn").addClass("color_ramps_on");
        $(".btn-group.color_ramps .btn.color_ramps_on").addClass("btn-primary");
        $(".btn-group.color_ramps .btn.color_ramps_off").removeClass("btn-primary");
    }
    else {
        $(".btn-group.tags_top_only .btn").removeClass("color_ramps_on");
        $(".btn-group.color_ramps .btn.color_ramps_on").removeClass("btn-primary");
        $(".btn-group.color_ramps .btn.color_ramps_off").addClass("btn-primary");
    }
    retrieveAndApplyTopicColors();
};

var changeRankingType = function(new_type) {
    var oldRankType = rank_type;
    rank_type = new_type;
    fetchLineGraph();
    retrieveAndApplyTopicColors(oldRankType);
}

// Pagination code
var update_pagination_buttons = function() {
    // Disable pagination buttons as appropriate.
    if ($(".custom-pager-pages li:first-child").hasClass("current")) {
        $(".custom-pager .prev, #main_content .prev").addClass("disabled");
    }
    else {
        $(".custom-pager .prev, #main_content .prev").removeClass("disabled");
    }
    if ($(".custom-pager-pages li:last-child").hasClass("current")) {
        $(".custom-pager .next, #main_content .next").addClass("disabled");
    }
    else {
        $(".custom-pager .next, #main_content .next").removeClass("disabled");
    }

    // Scroll to the current page.
    var current_page_position = (
        parseInt($(".custom-pager-pages li.current").get(0).offsetTop) -
        parseInt($(".custom-pager-pages").css("padding-top"))
    );
    $(".custom-pager-pages").animate({
        scrollTop: current_page_position + "px"
    }, 250);

    // Update svg page locator.
    // Yup, you need D3 for this.
    d3.selectAll("svg .tag_map_locator.current").classed("current", false);
    d3.selectAll("svg .tag_map_locator[data-page-index='" + page_index + "']").classed("current", true);
};

var init_pagination = function() {
    $(".custom-pager-pages li").remove();

    $.each(pages, function(index, value) {
        var $element = $("<li><a href='#' data-page-index='" + index + "'>" + (index + 1) + "</a></li>");
        if (index == page_index) {
            $element.addClass("current");
        }
        $(".custom-pager-pages").append($element);
    });

    update_pagination_buttons();
};

var prev_page = function() {
    if (page_index > 0) {
        change_to_page(page_index - 1);
    }
};

var next_page = function() {
    if (page_index < pages.length) {
        change_to_page(page_index + 1);
    }
};

var change_to_page = function(new_page_index) {
    $(".html_formatter").html(pages[new_page_index]);
    page_index = new_page_index;
    init_pagination();
    retrieveAndApplyTopicColors();
};

// Attach event listeners with jQuery.
(function() {
    updateTopicNames();

    $("#sidebar .btn-tag")
        .on("click", handleTagButtons)
        .on('contextmenu', function(event) {
            event.preventDefault();
            var $this = $(this);
            var topicNum = parseInt($this.attr('data-key').split('_')[1]);
            genTopicView(corpus_name, topicNum, '#topicDist', $this.text(), rank_type);
            $('#topicDistModal').modal('show');
        });

    $(".clear_all_tags").on("click", function() {
        $("#sidebar .btn-tag.active").each(handleTagButtons);
    });

    // Attach getTopicsForWordElement() to .html_formatter and delegate to span.token elements.
    $("#main_content").on("click", ".html_formatter > span[data-key!='!UNTAGGED']", getTopicsForWordElement);

    // Attach brushing events.
    $("#sidebar .btn-tag[data-key]").on("mouseover", function() {
        syncTopicBrushing($(this).attr("data-key"));
    }).on("mouseout", function() {
        endSyncTopicBrushing($(this).attr("data-key"));
    });

    // Attach cross-tab topic toggling
    window.addEventListener('storage', function() {
        if (event.key == corpus_name) {
            retrieveAndApplyTopicColors();
        }
    }, false);

    // Now the line graph should get an update on page load.
    fetchLineGraph();

    // Update Pagination -------------------------------------------------------
    page_index = 0;
    init_pagination();

    // Attach pagination events to .pagination li a.
    $(".custom-pager-pages").on("click", "li a[data-page-index]", function(e) {
        e.preventDefault();
        if ($(this).hasClass("current")) {
            return;
        }
        change_to_page(parseInt(
            $(this).attr("data-page-index")
        ));
    });

    $(".custom-pager a.prev, #main_content a.prev").on("click", function(e) {
        e.preventDefault();
        if ($(this).hasClass("disabled")) {
            return;
        }
        prev_page();
    });

    $(".custom-pager a.next, #main_content a.next").on("click", function(e) {
        e.preventDefault();
        if ($(this).hasClass("disabled")) {
            return;
        }
        next_page();
    });
    // End pagination ---------------------------------------------------------------

//    $("body").on(".popover rect", "mouseover", function() {
//        syncTopicBrushing($(this).attr("data-key"));
//    }).on(".popover rect", "mouseout", function() {
//        endSyncTopicBrushing($(this).attr("data-key"));
//    });

    // Also, attach the line graph events to any and all line graphs.
//    $(".topic_model_line_graph").each(attachLineGraphEventsToElement);

    // Initialize "Text Tagging Display" buttons.
    //changeTagDisplayMode(tags_top_only);
    changeColorRampsMode(color_ramps);

    $(".btn-group.tags_top_only .btn.btn-tags_top_only_on").click(function() {
        changeTagDisplayMode(true);
    });

    $(".btn-group.tags_top_only .btn.btn-tags_top_only_off").click(function() {
        changeTagDisplayMode(false);
    });

    $(".btn-group.color_ramps .btn.color_ramps_on").click(function() {
        changeColorRampsMode(true);
    });

    $(".btn-group.color_ramps .btn.color_ramps_off").click(function() {
        changeColorRampsMode(false);
    });

    $('#rankingTypeRadioGroup').change(function() {
        var selectedType = $('input[name=rankingType]:checked').attr('id');
        changeRankingType(selectedType);
    });

    retrieveAndApplyTopicColors();
}());
