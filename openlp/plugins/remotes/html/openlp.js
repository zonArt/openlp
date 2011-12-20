/*****************************************************************************
 * OpenLP - Open Source Lyrics Projection                                    *
 * ------------------------------------------------------------------------- *
 * Copyright (c) 2008-2010 Raoul Snyman                                      *
 * Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael    *
 * Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,      *
 * Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,    *
 * Jeffrey Smith, Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode     *
 * Woldsund                                                                  *
 * ------------------------------------------------------------------------- *
 * This program is free software; you can redistribute it and/or modify it   *
 * under the terms of the GNU General Public License as published by the     *
 * Free Software Foundation; version 2 of the License.                       *
 *                                                                           *
 * This program is distributed in the hope that it will be useful, but       *
 * WITHOUT ANY WARRANTY; without even the implied warranty of                *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General  *
 * Public License for more details.                                          *
 *                                                                           *
 * You should have received a copy of the GNU General Public License along   *
 * with this program; if not, write to the Free Software Foundation, Inc.,   *
 * 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA                     *
 *****************************************************************************/

window.OpenLP = {
  getElement: function(event) {
    var targ;
    if (!event) {
      var event = window.event;
    }
    if (event.target) {
      targ = event.target;
    }
    else if (event.srcElement) {
      targ = event.srcElement;
    }
    if (targ.nodeType == 3) {
      // defeat Safari bug
      targ = targ.parentNode;
    }
    return $(targ);
  },
  getSearchablePlugins: function (event) {
    $.getJSON(
      "/api/plugin/search",
      function (data, status) {
        var select = $("#search-plugin");
        select.html("");
        $.each(data.results.items, function (idx, value) {
          select.append("<option value='" + value[0] + "'>" + value[1] + "</option>");
        });
        select.selectmenu("refresh");
      }
    );
    return false;
  },
  loadService: function (event) {
    $.getJSON(
      "/api/service/list",
      function (data, status) {
        var ul = $("#service-manager > div[data-role=content] > ul[data-role=listview]");
        ul.html("");
        $.each(data.results.items, function (idx, value) {
          var li = $("<li data-icon=\"false\">").append(
            $("<a href=\"#\">").attr("value", parseInt(idx, 10)).text(value["title"]));
          li.attr("uuid", value["id"])
          li.children("a").click(OpenLP.setItem);
          ul.append(li);
        });
        ul.listview("refresh");
      }
    );
    return false;
  },
  loadController: function (event) {
    $.getJSON(
      "/api/controller/live/text",
      function (data, status) {
        var ul = $("#slide-controller > div[data-role=content] > ul[data-role=listview]");
        ul.html("");
        for (idx in data.results.slides) {
          var text = data.results.slides[idx]["tag"];
          if (text != "") text = text + ": ";
          text = text + data.results.slides[idx]["text"];
          text = text.replace(/\n/g, '<br />');
          var li = $("<li data-icon=\"false\">").append(
            $("<a href=\"#\">").attr("value", parseInt(idx, 10)).html(text));
          if (data.results.slides[idx]["selected"]) {
            li.attr("data-theme", "e");
          }
          li.children("a").click(OpenLP.setSlide);
          ul.append(li);
        }
        ul.listview("refresh");
      }
    );
    return false;
  },
  setItem: function (event) {
    var item = OpenLP.getElement(event);
    var id = item.attr("value");
    var text = JSON.stringify({"request": {"id": id}});
    $.getJSON(
      "/api/service/set",
      {"data": text},
      function (data, status) {
        $.mobile.changePage("#slide-controller");
        $("#service-manager > div[data-role=content] ul[data-role=listview] li").attr("data-theme", "c").removeClass("ui-btn-up-e").addClass("ui-btn-up-c");
        while (item[0].tagName != "LI") {
          item = item.parent();
        }
        item.attr("data-theme", "e").removeClass("ui-btn-up-c").addClass("ui-btn-up-e");
        $("#service-manager > div[data-role=content] ul[data-role=listview]").listview("refresh");
      }
    );
    return false;
  },
  setSlide: function (event) {
    var slide = OpenLP.getElement(event);
    var id = slide.attr("value");
    var text = JSON.stringify({"request": {"id": id}});
    $.getJSON(
      "/api/controller/live/set",
      {"data": text},
      function (data, status) {
        $("#slide-controller div[data-role=content] ul[data-role=listview] li").attr("data-theme", "c").removeClass("ui-btn-up-e").addClass("ui-btn-up-c");
        while (slide[0].tagName != "LI") {
          slide = slide.parent();
        }
        slide.attr("data-theme", "e").removeClass("ui-btn-up-c").addClass("ui-btn-up-e");
        $("#slide-controller div[data-role=content] ul[data-role=listview]").listview("refresh");
      }
    );
    return false;
  },
  pollServer: function () {
    $.getJSON(
      "/api/poll",
      function (data, status) {
        var prevItem = OpenLP.currentItem;
        OpenLP.currentSlide = data.results.slide;
        OpenLP.currentItem = data.results.item;
        if ($("#service-manager").is(":visible")) {
          $("#service-manager div[data-role=content] ul[data-role=listview] li").attr("data-theme", "c").removeClass("ui-btn-up-e").addClass("ui-btn-up-c");
          $("#service-manager div[data-role=content] ul[data-role=listview] li a").each(function () {
            var item = $(this);
            while (item[0].tagName != "LI") {
              item = item.parent();
            }
            if (item.attr("uuid") == OpenLP.currentItem) {
              item.attr("data-theme", "e").removeClass("ui-btn-up-c").addClass("ui-btn-up-e");
              return false;
            }
          });
          $("#service-manager div[data-role=content] ul[data-role=listview]").listview("refresh");
        }
        if ($("#slide-controller").is(":visible")) {
          if (prevItem != OpenLP.currentItem) {
            OpenLP.loadController();
            return;
          }
          var idx = 0;
          $("#slide-controller div[data-role=content] ul[data-role=listview] li").attr("data-theme", "c").removeClass("ui-btn-up-e").addClass("ui-btn-up-c");
          $("#slide-controller div[data-role=content] ul[data-role=listview] li a").each(function () {
            var item = $(this);
            if (idx == OpenLP.currentSlide) {
              while (item[0].tagName != "LI") {
                item = item.parent();
              }
              item.attr("data-theme", "e").removeClass("ui-btn-up-c").addClass("ui-btn-up-e");
              return false;
            }
            idx++;
          });
          $("#slide-controller div[data-role=content] ul[data-role=listview]").listview("refresh");
        }
      }
    );
  },
  nextItem: function (event) {
    $.getJSON("/api/service/next");
    return false;
  },
  previousItem: function (event) {
    $.getJSON("/api/service/previous");
    return false;
  },
  nextSlide: function (event) {
    $.getJSON("/api/controller/live/next");
    return false;
  },
  previousSlide: function (event) {
    $.getJSON("/api/controller/live/previous");
    return false;
  },
  blankDisplay: function (event) {
    $.getJSON("/api/display/hide");
    return false;
  },
  unblankDisplay: function (event) {
    $.getJSON("/api/display/show");
    return false;
  },
  showAlert: function (event) {
    var text = JSON.stringify({"request": {"text": $("#alert-text").val()}});
    $.getJSON(
      "/api/alert",
      {"data": text},
      function () {
        $("#alert-text").val("");
      }
    );
    return false;
  },
  search: function (event) {
    var text = "{\"request\": {\"text\": \"" + $("#search-text").val() + "\"}}";
    $.getJSON(
      "/api/" + $("#search-plugin").val() + "/search",
      {"data": text},
      function (data, status) {
        var ul = $("#search > div[data-role=content] > ul[data-role=listview]");
        ul.html("");
        if (data.results.items.length == 0) {
          var li = $("<li data-icon=\"false\">").text(translationStrings["no_results"]);
          ul.append(li);
        }
        else {
            $.each(data.results.items, function (idx, value) {
              ul.append($("<li>").append($("<a>").attr("href", "#options")
                  .attr("data-rel", "dialog").attr("data-transition", "pop")
                  .attr("value", value[0]).click(OpenLP.showOptions)
                  .text(value[1])));
            });
        }
        ul.listview("refresh");
      }
    );
    return false;
  },
  showOptions: function (event) {
    var element = OpenLP.getElement(event);
    console.log(element);
    $("#selected-item").val(element.attr("value"));
    return false;
  },
  goLive: function (event) {
    var id = $("#selected-item").val();
    var text = "{\"request\": {\"id\": " + id + "}}";
    $.getJSON(
      "/api/" + $("#search-plugin").val() + "/live",
      {"data": text}
    );
    $.mobile.changePage("#slide-controller");
    return false;
  },
  addToService: function (event) {
    var id = $("#selected-item").val();
    var text = JSON.stringify({"request": {"id": id}});
    $.getJSON(
      "/api/" + $("#search-plugin").val() + "/add",
      {"data": text},
      function () {
        history.back();
      }
    );
    $("#options").dialog("close");
    return false;
  }
}
// Service Manager
$("#service-manager").live("pagebeforeshow", OpenLP.loadService);
$("#service-refresh").live("click", OpenLP.loadService);
$("#service-top-next, #service-btm-next").live("click", OpenLP.nextItem);
$("#service-top-previous, #service-btm-previous").live("click", OpenLP.previousItem);
$("#service-top-blank, #service-btm-blank").live("click", OpenLP.blankDisplay);
$("#service-top-unblank, #service-btm-unblank").live("click", OpenLP.unblankDisplay);
// Slide Controller
$("#slide-controller").live("pagebeforeshow", OpenLP.loadController);
$("#controller-refresh").live("click", OpenLP.loadController);
$("#controller-top-next, #controller-btm-next").live("click", OpenLP.nextSlide);
$("#controller-top-previous, #controller-btm-previous").live("click", OpenLP.previousSlide);
$("#controller-top-blank, #controller-btm-blank").live("click", OpenLP.blankDisplay);
$("#controller-top-unblank, #controller-btm-unblank").live("click", OpenLP.unblankDisplay);
// Alerts
$("#alert-submit").live("click", OpenLP.showAlert);
// Search
$("#search-submit").live("click", OpenLP.search);
$("#search-text").live("keypress", function(event){
    if (event.which == 13) { OpenLP.search(event); }});
$("#go-live").live("click", OpenLP.goLive);
$("#add-to-service").live("click", OpenLP.addToService);
// Poll the server twice a second to get any updates.
OpenLP.getSearchablePlugins();
$.ajaxSetup({ cache: false });
setInterval("OpenLP.pollServer();", 500);
OpenLP.pollServer();
