/******************************************************************************
 * OpenLP - Open Source Lyrics Projection                                      *
 * --------------------------------------------------------------------------- *
 * Copyright (c) 2008-2013 Raoul Snyman                                        *
 * Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      *
 * Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      *
 * Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   *
 * Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          *
 * Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             *
 * Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              *
 * Frode Woldsund, Martin Zibricky                                             *
 * --------------------------------------------------------------------------- *
 * This program is free software; you can redistribute it and/or modify it     *
 * under the terms of the GNU General Public License as published by the Free  *
 * Software Foundation; version 2 of the License.                              *
 *                                                                             *
 * This program is distributed in the hope that it will be useful, but WITHOUT *
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       *
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    *
 * more details.                                                               *
 *                                                                             *
 * You should have received a copy of the GNU General Public License along     *
 * with this program; if not, write to the Free Software Foundation, Inc., 59  *
 * Temple Place, Suite 330, Boston, MA 02111-1307 USA                          *
 ******************************************************************************/
window.OpenLP = {
  loadSlide: function (event) {
    $.getJSON(
      "/main/image",
      function (data, status) {
        var img = document.getElementById('image');
        img.src = data.results.slide_image;
        img.style.display = 'block';
      }
    );
  },
  pollServer: function () {
    $.getJSON(
      "/main/poll",
      function (data, status) {
        if (OpenLP.slideCount != data.results.slide_count) {
          OpenLP.slideCount = data.results.slide_count;
          OpenLP.loadSlide();
        }
      }
    );
  }
}
$.ajaxSetup({ cache: false });
setInterval("OpenLP.pollServer();", 500);
OpenLP.pollServer();

