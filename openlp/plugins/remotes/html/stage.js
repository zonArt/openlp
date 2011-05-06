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
  loadSlides: function (event) {
    $.getJSON(
      "/api/controller/live/text",
      function (data, status) {
        OpenLP.currentSlides = data.results.slides;
        OpenLP.currentSlide = 0;
        for (idx in data.results.slides) {
          if (data.results.slides[idx]["selected"]) {
            OpenLP.currentSlide = parseInt(idx, 10);
            break;
          }
        }
        OpenLP.updateSlide();
      }
    );
  },
  updateSlide: function() {
    var div = $("#currentslide");
    div.html(OpenLP.currentSlides[OpenLP.currentSlide]["text"]);
    var divnext = $("#nextslide");
    if (OpenLP.currentSlide < OpenLP.currentSlides.length - 1) 
        divnext.html(OpenLP.currentSlides[OpenLP.currentSlide + 1]["text"]);
    else
        divnext.html("");
  },
  updateClock: function() {
    var div = $("#clock");
    var t = new Date(); 
    var h = t.getHours();
    if (h > 12) 
        h = h - 12;
    var m = t.getMinutes();
    if (m.length == 1)
        m = '0' + m;
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
