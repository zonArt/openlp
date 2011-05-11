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
        OpenLP.currentTags = Array();
        var div = $("#verseorder");
        div.html("");
        var tag = "";
        var tags = 0;
        for (idx in data.results.slides) {
          idx = parseInt(idx, 10);
          var prevtag = tag;
          tag = data.results.slides[idx]["tag"];
          if (tag != prevtag) {
            tags = tags + 1;
            div.append("&nbsp;<span>");       
            $("#verseorder span").last().attr("id", "tag" + tags).text(tag);
          }
          OpenLP.currentTags[idx] = tags;
          if (data.results.slides[idx]["selected"]) 
            OpenLP.currentSlide = idx;
        }
        OpenLP.loadService();
      }
    );
  },
  updateSlide: function() {
    $("#verseorder span").removeClass("currenttag");
    $("#tag" + OpenLP.currentTags[OpenLP.currentSlide]).addClass("currenttag");
    var slide = OpenLP.currentSlides[OpenLP.currentSlide];
    var text = slide["text"];
    text = text.replace(/\n/g, '<br />');
    $("#currentslide").html(text);
    text = "";
    if (OpenLP.currentSlide < OpenLP.currentSlides.length - 1) {
      for (var idx = OpenLP.currentSlide + 1; idx < OpenLP.currentSlides.length; idx++) {
        var prevslide = slide;
        slide = OpenLP.currentSlides[idx];
        if (slide["tag"] != prevslide["tag"])
            text = text + '<p class="nextslide">';
        text = text + slide["text"]; 
        if (slide["tag"] != prevslide["tag"])
            text = text + '</p>';
        else
            text = text + '<br />';
      }
      text = text.replace(/\n/g, '<br />');
      $("#nextslide").html(text);
    }
    else
      text = '<p class="nextslide">Next: ' + OpenLP.nextSong + '</p>';
      $("#nextslide").html(text);
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
