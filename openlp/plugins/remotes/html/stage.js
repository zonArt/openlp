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
  loadService: function (event) {
    $.getJSON(
      "/api/service/list",
      function (data, status) {
        OpenLP.nextSong = "";
        $("#notes").html("");
        for (idx in data.results.items) {
          idx = parseInt(idx, 10);
          if ((data.results.items[idx]["selected"]) && 
            (data.results.items.length > idx + 1)) {
            $("#notes").html(data.results.items[idx]["notes"]);
            OpenLP.nextSong = data.results.items[idx + 1]["title"];
            break;
          }
        }
        OpenLP.updateSlide();
      }
    );
  },
  loadSlides: function (event) {
    $.getJSON(
      "/api/controller/live/text",
      function (data, status) {
        OpenLP.currentSlides = data.results.slides;
        OpenLP.currentSlide = 0;
        var div = $("#verseorder");
        div.html("");
        for (idx in data.results.slides) {
          idx = parseInt(idx, 10);
          div.append("&nbsp;<span>");
          var tag = data.results.slides[idx]["tag"];
          if (tag == 'None')
            tag = idx;
          $("#verseorder span").last().attr("id", "tag" + idx).text(tag);
          if (data.results.slides[idx]["selected"]) 
            OpenLP.currentSlide = idx;
        }
        OpenLP.loadService();
      }
    );
  },
  updateSlide: function() {
    $("#verseorder span").removeClass("currenttag");
    $("#tag" + OpenLP.currentSlide).addClass("currenttag");
    $("#currentslide").html(OpenLP.currentSlides[OpenLP.currentSlide]["text"]);
    if (OpenLP.currentSlide < OpenLP.currentSlides.length - 1) 
      $("#nextslide").html(OpenLP.currentSlides[OpenLP.currentSlide + 1]["text"]);
    else 
      $("#nextslide").html("Next: " + OpenLP.nextSong);
  },
  updateClock: function() {
    var div = $("#clock");
    var t = new Date(); 
    var h = t.getHours();
    if (h > 12) 
      h = h - 12;
    var m = t.getMinutes();
    if (m < 10)
      m = '0' + m + '';
    div.html(h + ":" + m);
  },
  pollServer: function () {
    $.getJSON(
      "/api/poll",
      function (data, status) {
        OpenLP.updateClock();
        if (OpenLP.currentItem != data.results.item) {
          OpenLP.currentItem = data.results.item;
          OpenLP.loadSlides();
        } 
        else if (OpenLP.currentSlide != data.results.slide) {
          OpenLP.currentSlide = parseInt(data.results.slide, 10);
          OpenLP.updateSlide();
        }
      }
    );
  }
}
$.ajaxSetup({ cache: false });
setInterval("OpenLP.pollServer();", 500);
OpenLP.pollServer();
