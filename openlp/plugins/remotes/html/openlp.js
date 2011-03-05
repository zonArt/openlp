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

$("#service-manager").live("pagebeforeshow", function (event) {
  $.getJSON(
    "/api/service/list",
    function (data, status) {
      var ul = $("<ul data-role=\"listview\" data-inset=\"true\">");
      for (idx in data.results) {
        var li = $("<li data-icon=\"false\">").append(
          $("<a href=\"#\">").text(data.results[idx]["title"]));
        ul.append(li);
      }
      $("#service-manager > div[data-role=content]").html(ul);
      $("#service-manager").refresh();
    }
  );
});

$("#slide-controller").live("pagebeforeshow", function (event) {
  $.getJSON(
    "/api/controller/live/text",
    function (data, status) {
      var ul = $("<ul data-role=\"listview\" data-inset=\"true\">");
      for (idx in data.results.slides) {
        var li = $("<li data-icon=\"false\">").append(
          $("<a href=\"#\">").html(data.results.slides[idx]["text"]));
        if (data.results.slides[idx]["selected"]) {
          li.attr("data-theme", "e");
        }
        ul.append(li);
      }
      $("#slide-controller div[data-role=content]").html(ul);
      $("#slide-controller").refresh();
    }
  );
});
