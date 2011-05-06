/*****************************************************************************
 * OpenLP - Open Source Lyrics Projection                                    *
 * ------------------------------------------------------------------------- *
 * Copyright (c) 2008-2010 Raoul Snyman                                      *
 * Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael    *
 * Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,      *
 * Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,    *
 * Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund           *
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
  },
  loadController: function (event) {
    $.getJSON(
      "/api/controller/live/text",
      function (data, status) {
        var ul = $("#slide-controller > div[data-role=content] > ul[data-role=listview]");
        ul.html("");
        for (idx in data.results.slides) {
          var li = $("<li data-icon=\"false\">").append(
            $("<a href=\"#\">").attr("value", parseInt(idx, 10)).html(data.results.slides[idx]["text"]));
          if (data.results.slides[idx]["selected"]) {
            li.attr("data-theme", "e");
          }
          li.children("a").click(OpenLP.setSlide);
          ul.append(li);
        }
        ul.listview("refresh");
      }
    );
  },
  setItem: function (event) {
    var item = OpenLP.getElement(event);
    var id = item.attr("value");
    var text = JSON.stringify({"request": {"id": id}});
    $.getJSON(
      "/api/service/set",
      {"data": text},
      function (data, status) {
        $("#service-manager > div[data-role=content] ul[data-role=listview] li").attr("data-theme", "c").removeClass("ui-btn-up-e").addClass("ui-btn-up-c");
        while (item[0].tagName != "LI") {
          item = item.parent();
        }
        item.attr("data-theme", "e").removeClass("ui-btn-up-c").addClass("ui-btn-up-e");
        $("#service-manager > div[data-role=content] ul[data-role=listview]").listview("refresh");
      }
    );
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
  },
  pollServer: function () {
    $.getJSON(
      "/api/poll",
      function (data, status) {
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
  }
}
// Service Manager
$("#service-manager").live("pagebeforeshow", OpenLP.loadService);
$("#service-refresh").live("click", OpenLP.loadService);
$("#service-next").live("click", OpenLP.nextItem);
$("#service-previous").live("click", OpenLP.previousItem);
$("#service-blank").live("click", OpenLP.blankDisplay);
$("#service-unblank").live("click", OpenLP.unblankDisplay);
// Slide Controller
$("#slide-controller").live("pagebeforeshow", OpenLP.loadController);
$("#controller-refresh").live("click", OpenLP.loadController);
$("#controller-next").live("click", OpenLP.nextSlide);
$("#controller-previous").live("click", OpenLP.previousSlide);
$("#controller-blank").live("click", OpenLP.blankDisplay);
$("#controller-unblank").live("click", OpenLP.unblankDisplay);
// Alerts
$("#alert-submit").live("click", OpenLP.showAlert);
// Poll the server twice a second to get any updates.
setInterval("OpenLP.pollServer();", 500);
OpenLP.pollServer();
