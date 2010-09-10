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

OpenLP.Namespace.create("OpenLP.Service", {
    addServiceItem: function (elem, item)
    {
        var trow = $("<tr>")
            .attr("id", "item-" + item.id)
            .addClass("item")
            .append($("<td>").text(item.tag))
            .append($("<td>").text(item.tag.replace(/\n/g, "<br />")));
        return false;
    },
    sendLive: function (e)
    {
        var elem = OpenLP.Events.getElement(e);
        var row = elem.attr("id").substr(5);
        elem.addStyle("font-weight", "bold");
        return false;
    }
});

OpenLP.Events.load(function (){
    OpenLP.Events.liveClick(".item", OpenLP.Service.sendLive);
});