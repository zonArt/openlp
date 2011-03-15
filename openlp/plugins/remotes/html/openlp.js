/*****************************************************************************
 * OpenLP - Open Source Lyrics Projection                                    *
 * ------------------------------------------------------------------------- *
 * Copyright (c) 2008-2010 Raoul Snyman                                      *
 * Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael    *
 * Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin    *
 * Thompson, Jon Tibble, Carsten Tinggaard                                   *
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
        for (idx in data.results) {
          var li = $("<li data-icon=\"false\">").append(
            $("<a href=\"#\">").attr("value", idx + 1).text(data.results[idx]["title"]));
          li.children("a").click(OpenLP.setItem);
          ul.append(li);
        }
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
            $("<a href=\"#\">").attr("value", idx + 1).html(data.results.slides[idx]["text"]));
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
  updateItem: function () {
    $.getJSON(
      "/api/poll",
      function (data, status) {
        var idx;
        var len = $("#slide-controller div[data-role=content] ul[data-role=listview] li").length;
        for (idx = 0; idx < len; idx++) {
          if (idx == data.results.slide) {
            $($("#slide-controller div[data-role=content] ul[data-role=listview] li")[idx]).attr("data-theme", "e").removeClass("ui-btn-up-c").addClass("ui-btn-up-e");
          }
          else {
            $($("#slide-controller div[data-role=content] ul[data-role=listview] li")[idx]).attr("data-theme", "c").removeClass("ui-btn-up-e").addClass("ui-btn-up-c");
          }
        }
        $("#slide-controller div[data-role=content] ul[data-role=listview]").listview("refresh");
      }
    );
  }
}

$("#service-manager").live("pagebeforeshow", OpenLP.loadService);
$("#slide-controller").live("pagebeforeshow", OpenLP.loadController);
setInterval("OpenLP.updateItem();", 500);
OpenLP.updateItem();
