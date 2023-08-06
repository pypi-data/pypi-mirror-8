// Hive Metrium System
// Copyright (C) 2008-2014 Hive Solutions Lda.
//
// This file is part of Hive Metrium System.
//
// Hive Metrium System is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Hive Metrium System is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Hive Metrium System. If not, see <http://www.gnu.org/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2008-2014 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

(function(jQuery) {
    jQuery.fn.uapply = function(options) {
        // sets the jquery matched object
        var matchedObject = this;

        var pusher = jQuery(".pusher", matchedObject);
        pusher.upusher();

        var dashboard = jQuery(".dashboard", matchedObject);
        dashboard.udashboard();

        var progress = jQuery(".progress", matchedObject);
        progress.uprogress();

        var lineChart = jQuery(".line-chart", matchedObject);
        lineChart.ulinechart();
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.udashboard = function(options) {
        var MESSAGE_TIMEOUT = 15000;
        var BOARD_TIMEOUT = 30000;
        var LINE_HEIGHT = 49;

        var matchedObject = this;
        var pusher = jQuery(".pusher", matchedObject);
        var status = jQuery(".status", matchedObject);

        pusher = pusher.data("pusher");
        if (!pusher) {
            return matchedObject;
        }

        var initialize = function() {
            _start();
            _layout();
            _boards();
            _general();
            _modules();

        };

        var _start = function() {
            var connection = pusher.connection;
            var global = pusher.subscribe("global");
            matchedObject.data("global", global);
            var video = jQuery(".video", matchedObject);

            matchedObject.bind("message",
                    function(event, type, owner, message) {
                        _showMessage(type, owner, message);
                        _playSound("/static/sounds/" + type + ".mp3");
                    });

            connection.bind("connecting", function() {
                    });

            connection.bind("connected", function() {
                        _hideError();
                    });

            connection.bind("unavailable", function() {
                        _showError();
                    });

            connection.bind("disconnected", function() {
                        _showError();
                    });

            connection.bind("error", function(error) {
                        _showError();
                    });

            global.bind("video.open", function(data) {
                        var url = data.url;
                        _showVideo(url);
                    });

            video.bind("ended", function() {
                        var element = jQuery(this);
                        var overlay = jQuery(".overlay");

                        overlay.fadeOut(250);
                        element.fadeOut(250);
                    });
        };

        var _layout = function() {
            var _html = jQuery("html");
            _html.css("overflow-y", "auto");
        };

        var _general = function() {
            jQuery.ajax({
                        url : "/state",
                        beforeSend : function() {
                            _hide();
                        },
                        success : function(data) {
                            _onState(data);
                            _show();
                        },
                        error : function() {
                            _show();
                        }
                    });
        };

        var _boards = function() {
            var boards = jQuery(".boards > .board", matchedObject);
            boards.hide();

            var first = jQuery(boards[0]);
            first.show();

            matchedObject.data("index", 0);
            if (boards.length <= 1) {
                return;
            }

            setInterval(function() {
                        var index = matchedObject.data("index");
                        index = index + 1 >= boards.length ? 0 : index + 1;
                        _showBoard(index);
                    }, BOARD_TIMEOUT);
        };

        var _hide = function() {
            matchedObject.css("visibility", "hidden");
        };

        var _show = function() {
            matchedObject.css("visibility", "visible");
        };

        var _onState = function(state) {
            var global = matchedObject.data("global");
            for (var module in state) {
                var events = state[module];

                for (var name in events) {
                    var event = events[name];
                    for (var index = event.length - 1; index >= 0; index--) {
                        var _event = event[index];
                        global.emit(name, _event);
                    }
                }
            }
        };

        var _modules = function() {
            matchedObject.udate();
            matchedObject.ulog();
            matchedObject.uglobal();
            matchedObject.upending();
        };

        var _showBoard = function(index) {
            var boards = jQuery(".boards > .board:visible", matchedObject);
            var sections = jQuery("ul.sections > li.active", matchedObject);

            boards.fadeOut(350, function() {
                        var board = jQuery(".boards > .board:nth-child("
                                        + (index + 1) + ")", matchedObject);
                        var section = jQuery("ul.sections > li:nth-child("
                                        + (index + 1) + ")", matchedObject);

                        sections.removeClass("active");
                        section.addClass("active");
                        board.fadeIn(350);

                        matchedObject.data("index", index);
                    });
        };

        var _showVideo = function(link) {
            var isVisible = matchedObject.css("visibility") == "visible";
            if (!isVisible) {
                return;
            }

            var overlay = jQuery(".overlay");
            var video = jQuery(".video", matchedObject);

            video.html(link);
            video.uxvideo();

            overlay.fadeIn(350);
            video.fadeIn(350);
            video.uxcenter(0, 0, false, false, false, true);
        };

        var _showMessage = function(type, author, contents) {
            var isVisible = matchedObject.css("visibility") == "visible";
            if (!isVisible) {
                return;
            }

            var timeoutP = matchedObject.data("timeout");
            var intervalP = matchedObject.data("interval");
            if (timeoutP) {
                clearTimeout(timeoutP);
            }
            if (intervalP) {
                clearInterval(intervalP);
            }

            var _message = jQuery("> .message", matchedObject);
            var _author = jQuery("> .author", _message);
            var _contents = jQuery("> .contents", _message);

            _message.show();
            _message.scrollTop(0);
            _message.hide();

            _author.html(author);
            _contents.html(contents);

            _message.removeClass("info");
            _message.removeClass("success");
            _message.removeClass("warning");
            _message.removeClass("error");

            _message.addClass(type);
            _message.fadeIn(200);

            var paddingVertical = _message.outerHeight() - _message.height();
            var lines = ((_message[0].scrollHeight - paddingVertical) / LINE_HEIGHT);
            var timing = MESSAGE_TIMEOUT / lines;

            var interval = setInterval(function() {
                        _message.animate({
                                    scrollTop : "+=" + LINE_HEIGHT + "px"
                                }, 300);
                    }, timing);

            var timeout = setTimeout(function() {
                        clearInterval(interval);
                        _message.fadeOut(150);
                    }, MESSAGE_TIMEOUT);

            matchedObject.data("timeout", timeout);
            matchedObject.data("interval", interval);
        };

        var _playSound = function(path) {
            var isVisible = matchedObject.css("visibility") == "visible";
            if (!isVisible) {
                return;
            }

            var sound = jQuery(".sound", matchedObject);
            var soundElement = sound[0];
            sound.attr("src", path);
            soundElement.play();
        };

        var _showError = function() {
            var overlay = jQuery(".overlay");
            var errorPanel = jQuery(".error-panel");
            overlay.fadeIn(350);
            errorPanel.fadeIn(350);
            errorPanel.uxcenter(0, 0, false, false, false, true);
        };

        var _hideError = function() {
            var overlay = jQuery(".overlay");
            var errorPanel = jQuery(".error-panel");
            overlay.fadeOut(200);
            errorPanel.fadeOut(200);
        };

        initialize();
        return matchedObject;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.udate = function(options) {

        var TIMEOUT = 10000;

        var DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Starturday"];
        var DAYS_PT = ["Domnigo", "Segunda-feira", "Terça-Feira",
                "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado"];

        var MONTHS = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November",
                "December"];
        var MONTHS_PT = ["Janeiro", "Febreiro", "Março", "Abril", "Maio",
                "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro",
                "Dezembro"];

        var matchedObject = this;

        var initialize = function() {
            _start();
        };

        var _start = function() {
            _update();
            setInterval(function() {
                        _update();
                    }, TIMEOUT);
        };

        var _update = function() {
            var date = jQuery(".date", matchedObject);
            var weekDay = jQuery(".week-day", date);
            var day = jQuery(".day", date);
            var time = jQuery(".time", date);

            var _date = new Date();
            var dayIndex = _date.getDay();
            var dayString = DAYS_PT[dayIndex];

            var dayMonth = _date.getDate();
            var dayMonthS = _toString(dayMonth);
            var month = _date.getMonth();
            var monthS = MONTHS_PT[month];
            var dayLine = dayMonthS + " " + monthS;

            var hours = _date.getHours();
            var minutes = _date.getMinutes();
            var timeLine = _toString(hours) + ":" + _toString(minutes);

            weekDay.html(dayString);
            day.html(dayLine);
            time.html(timeLine);
        };

        var _toString = function(value, length) {
            length = length || 2;
            value = String(value);

            for (var index = value.length; index < length; index++) {
                value = "0" + value;
            }
            return value;
        };

        initialize();
        return matchedObject;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.uglobal = function(options) {
        var matchedObject = this;

        var initialize = function() {
            _start();
        };

        var _start = function() {
            var global = matchedObject.data("global");
            global.bind("omni.sales_total", function(data) {
                        _updateSalesTotal(data.sales_total);
                    });
            global.bind("omni.sales_data", function(data) {
                        _updateSalesData(data.sales_data);
                    });
            global.bind("omni.sales_stores", function(data) {
                        _updateSalesStores(data.sales_stores);
                    });
            global.bind("omni.top_stores", function(data) {
                        _updateTopStores(data.top_stores);
                    });
            global.bind("omni.top_employees", function(data) {
                        _updateTopEmployees(data.top_employees);
                    });
        };

        var _updateSalesTotal = function(salesTotal) {
            var _salesTotal = jQuery(".sales-total", matchedObject);
            var value = jQuery(".value", _salesTotal);
            var subValue = jQuery(".sub-value", _salesTotal);
            var progress = jQuery(".progress", _salesTotal);

            var previous = salesTotal[0];
            var current = salesTotal[1];
            var ratio = current / previous;
            ratio = ratio > 1.0 ? 1.0 : ratio;
            ratio *= 100;
            ratio = Math.floor(ratio);
            var ratioS = String(ratio);
            previous = jQuery.uxround(previous / 1000, 1);
            current = jQuery.uxround(current / 1000, 1);
            previous = previous.toFixed(1) + "K";
            current = current.toFixed(1) + "K";

            value.text(current);
            subValue.text(previous);

            progress.attr("data-value", ratioS);
            progress.uprogress();
        };

        var _updateSalesData = function(salesData) {
            var _salesData = jQuery(".sales-data", matchedObject);
            var lineChart = jQuery(".line-chart", _salesData);
            var salesDataS = String(salesData);

            lineChart.attr("data-values", salesDataS);
            lineChart.ulinechart();
        };

        var _updateSalesStores = function(salesStores, marker) {
            var _salesStores = jQuery(".sales-stores", matchedObject);
            var tableBody = jQuery("table > tbody", _salesStores);
            tableBody.empty();

            var size = salesStores.length > 5 ? 5 : salesStores.length;

            for (var index = 0; index < size; index++) {
                var item = salesStores[index];
                var current = item[0].toFixed(2);
                var previous = item[1].toFixed(2);
                var name = item[2];
                var row = jQuery("<tr>" + "<td>" + name + "</td>"
                        + "<td class=\"value\">" + previous + "</td>"
                        + "<td class=\"value\">" + current + "</td>" + "</tr>");
                if (marker) {
                    row.append("<td class=\"marker\">"
                            + "<div class=\"up color\"></div>" + "</td>");
                }
                tableBody.append(row);
            }
        };

        var _updateTopStores = function(topStores) {
            var _topStores = jQuery(".top-stores", matchedObject);
            var bubleContent = jQuery(".bubble-content", _topStores);
            bubleContent.empty();

            var size = topStores.length > 3 ? 3 : topStores.length;

            for (var index = 0; index < size; index++) {
                var item = topStores[index];
                var value = String(item[0]);
                var name = item[1];
                var bubleContents = jQuery("<div class=\"bubble-contents\">"
                        + "<div class=\"value\">" + value + "</div>"
                        + "<div class=\"title\">" + name + "</div>" + "</div>");
                index != 0 && bubleContents.addClass("double");
                bubleContent.append(bubleContents);
            }
        };

        var _updateTopEmployees = function(topEmployees) {
            var _topEmployees = jQuery(".top-employees", matchedObject);
            var topContent = jQuery(".top-content", _topEmployees);
            topContent.empty();

            var size = topEmployees.length > 3 ? 3 : topEmployees.length;

            for (var index = 0; index < size; index++) {
                var item = topEmployees[index];
                var amount = String(item[0]);
                var number = String(item[1]);
                var name = item[2];
                var imageUrl = item[3];
                var topContents = jQuery("<div class=\"top-contents\">"
                        + "<div class=\"rank\">" + String(index + 1) + "</div>"
                        + "<div class=\"picture\">" + "<img src=\"" + imageUrl
                        + "\" />" + "</div>" + "<div class=\"details\">"
                        + "<div class=\"name\">" + name + "</div>"
                        + "<div class=\"value\">" + number + "x - </div>"
                        + "<div class=\"value\">" + amount + "</div>"
                        + "</div>" + "</div>");
                topContent.append(topContents);
            }
        };

        initialize();
        return matchedObject;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.ulinechart = function(options) {
        var PADDING_TOP = 32;
        var PADDING_LEFT = 5;
        var PADDING_RIGHT = 5;

        var matchedObject = this;

        var initialize = function() {
            _start();
        };

        var _start = function() {
            if (matchedObject.length == 0) {
                return;
            }

            var width = matchedObject.width();
            var height = matchedObject.height();

            width && matchedObject.attr("width", width);
            height && matchedObject.attr("height", height);

            var widthS = matchedObject.attr("width");
            var heightS = matchedObject.attr("height");

            width = parseInt(widthS);
            height = parseInt(heightS);

            var values = matchedObject.attr("data-values") || "";
            values = values.split(",");
            for (var index = 0; index < values.length; index++) {
                var value = values[index];
                values[index] = parseFloat(value);
            }

            var maxValue = 0;

            for (var index = 0; index < values.length; index++) {
                var value = values[index];
                maxValue = value > maxValue ? value : maxValue;
            }

            var canvas = matchedObject[0];
            var context = canvas.getContext("2d");
            context.setTransform(1, 0, 0, 1, 0, 0);
            context.clearRect(0, 0, width, height);

            var widthChart = width - PADDING_LEFT - PADDING_RIGHT;
            var heightChart = height - PADDING_TOP;
            var stepWidth = widthChart / (values.length - 1);
            var xPosition = PADDING_LEFT;

            for (var index = 0; index < values.length; index++) {
                var value = values[index];
                var yPosition = height - (value * heightChart / maxValue);

                if (index != 0) {
                    context.beginPath();
                    context.strokeStyle = "#ffffff";
                    context.moveTo(xPositionP, yPositionP);
                    context.lineTo(xPosition, yPosition);
                    context.lineWidth = 4;
                    context.stroke();

                    context.beginPath();
                    context.fillStyle = "rgba(255, 255, 255, 0.2)";
                    context.moveTo(xPositionP, yPositionP);
                    context.lineTo(xPosition, yPosition);
                    context.lineTo(xPosition, height);
                    context.lineTo(xPositionP, height);
                    context.closePath();
                    context.fill();
                }

                if (index != 0 && index != values.length - 1) {
                    context.beginPath();
                    context.strokeStyle = "rgba(255, 255, 255, 0.3)";
                    context.lineWidth = 2;
                    context.dashedLine(xPosition, yPosition, xPosition, height,
                            [6, 4]);
                    context.stroke();
                }

                context.beginPath();
                context.fillStyle = "#ffffff";
                context.arc(xPosition, yPosition, 5, 0, 2 * Math.PI, false);
                context.fill();

                var xPositionP = xPosition;
                var yPositionP = yPosition;

                xPosition += stepWidth;
            }
        };

        initialize();
        return matchedObject;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.ulog = function(options) {
        var matchedObject = this;

        var initialize = function() {
            _start();
        };

        var _start = function() {
            var global = matchedObject.data("global");
            global.bind("log.message", function(data) {
                        _new(data.contents);
                    });
        };

        var _new = function(contents) {
            var date = new Date(contents.timestamp * 1000);
            var hours = date.getHours();
            var minutes = date.getMinutes();
            var timeLine = _toString(hours) + ":" + _toString(minutes);

            var context = jQuery(".context", matchedObject);
            var news = jQuery(".news", context);
            var item = "<div class=\"news-item\">" + "<div class=\"title\">"
                    + "<span class=\"time\">" + timeLine + "</span>"
                    + "<span class=\"message\">" + contents.owner + "</span>"
                    + "<span class=\"marker " + contents.type + "\"></span>"
                    + "</div>" + "<div class=\"message\">" + contents.message
                    + "</div>" + "</div>";
            news.prepend(item);

            var newsElement = news[0];

            matchedObject.trigger("message", [contents.type, contents.owner,
                            contents.message]);

            while (true) {
                var overflows = newsElement.scrollHeight > newsElement.clientHeight;
                if (!overflows) {
                    break;
                }

                var lastChild = jQuery("> :last-child", news);
                lastChild.remove();
            }
        };

        var _toString = function(value, length) {
            length = length || 2;
            value = String(value);

            for (var index = value.length; index < length; index++) {
                value = "0" + value;
            }
            return value;
        };

        initialize();
        return matchedObject;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.upending = function(options) {
        var matchedObject = this;

        var initialize = function() {
            _start();
        };

        var _start = function() {
            var global = matchedObject.data("global");
            global.bind("pending.update", function(data) {
                        _update(data.pendings);
                    });
        };

        var _update = function(pendings) {
            var _pending = jQuery(".pending", matchedObject);

            var items = _pending.children();
            items.remove()

            for (var index = 0; index < pendings.length; index++) {
                var item = pendings[index];
                _pending.append("<li class=\"" + item.severity + "\">"
                        + "<span class=\"pre\">" + item.pre + "</span>"
                        + "<span class=\"description\">" + item.description
                        + "</span>" + "<span class=\"author\">" + item.author
                        + "</span>" + "<span class=\"marker\"></div>" + "</li>");
            }
        };

        initialize();
        return matchedObject;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.uprogress = function(options) {
        var matchedObject = this;

        var initialize = function() {
            _start();
        };

        var _start = function() {
            if (matchedObject.length == 0) {
                return;
            }

            var width = matchedObject.width();
            var height = matchedObject.height();

            width && matchedObject.attr("width", width);
            height && matchedObject.attr("height", height);

            var widthS = matchedObject.attr("width");
            var heightS = matchedObject.attr("height");

            width = parseInt(widthS);
            height = parseInt(heightS);

            var value = matchedObject.attr("data-value");
            var target = matchedObject.attr("data-target");

            value = parseInt(value);
            target = target ? parseInt(target) : null;

            var valueP = value * 2.0 / 100.0;
            var targetP = target ? (target - value) * 2.0 / 100.0 : 0.0;
            var remainingP = 2.0 - targetP - valueP;

            var canvas = matchedObject[0];
            var context = canvas.getContext("2d");
            context.setTransform(1, 0, 0, 1, 0, 0);
            context.clearRect(0, 0, width, height);

            var centerX = width / 2;
            var centerY = height / 2;
            var lower = width > height ? height : width;
            var radius = (lower / 2) - 18;

            context.translate(centerX, centerY);
            context.rotate(Math.PI / 2 * -1);

            context.beginPath();
            context.arc(0, 0, radius, 0, valueP * Math.PI, false);
            context.lineWidth = 12;
            context.strokeStyle = "#d6de23";
            context.stroke();
            context.rotate(valueP * Math.PI);

            if (target) {
                context.beginPath();
                context.arc(0, 0, radius, 0, targetP * Math.PI, false);
                context.lineWidth = 12;
                context.strokeStyle = "#ee4036";
                context.stroke();
                context.rotate(targetP * Math.PI);
            }

            context.beginPath();
            context.arc(0, 0, radius, 0, remainingP * Math.PI, false);
            context.lineWidth = 12;
            context.strokeStyle = "rgba(255, 255, 255, 0.6)";
            context.stroke();
        };

        initialize();
        return matchedObject;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.upusher = function(options) {
        var matchedObject = this;
        matchedObject.each(function() {
                    var element = jQuery(this);
                    var key = element.attr("data-key");
                    if (!key) {
                        return;
                    }

                    var pusher = new Pusher(key);
                    element.data("pusher", pusher);
                });
        return matchedObject;
    };
})(jQuery);

jQuery(document).ready(function() {
            var _body = jQuery("body");
            _body.bind("applied", function(event, base) {
                        base.uapply();
                    });
        });
