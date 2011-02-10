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

window["OpenLP"] = {
  Namespace: {
    /**
     * Create a Javascript namespace.
     * Based on: http://code.google.com/p/namespacedotjs/
     * Idea behind this is to created nested namespaces that are not ugly.
     */
    create: function (name, attributes) {
      var parts = name.split('.'),
      ns = window,
      i = 0;
      // find the deepest part of the namespace
      // that is already defined
      for(; i < parts.length && parts[i] in ns; i++)
        ns = ns[parts[i]];
      // initialize any remaining parts of the namespace
      for(; i < parts.length; i++)
        ns = ns[parts[i]] = {};
      // copy the attributes into the namespace
      for (var attr in attributes)
        ns[attr] = attributes[attr];
    },
    exists: function (namespace) {
      /**
       * Determine the namespace of a page
       */
      page_namespace = $ScribeEngine.Namespace.get_page_namespace();
      return (namespace == page_namespace);
    },
    get_page_namespace: function () {
      return $("#content > h2").attr("id");
    }
  }
};

Array.prototype.append = function (elem) {
  this[this.length] = elem;
}

OpenLP.Namespace.create("OpenLP.Events", {
  // Local variables
  onload_functions: Array(),
  // Functions
  bindLoad: function (func) {
    this.onload_functions.append(func);
  },
  bindClick: function (selector, func) {
    $(selector).bind("click", func);
  },
  bindChange: function (selector, func) {
    $(selector).bind("change", func);
  },
  bindSubmit: function (selector, func) {
    $(selector).bind("submit", func);
  },
  bindBlur: function (selector, func) {
    $(selector).bind("blur", func);
  },
  bindPaste: function (selector, func) {
    $(selector).bind("paste", func);
  },
  bindKeyUp: function (selector, func) {
    $(selector).bind("keyup", func);
  },
  bindKeyDown: function (selector, func) {
    $(selector).bind("keydown", func);
  },
  bindKeyPress: function (selector, func) {
    $(selector).bind("keypress", func);
  },
  bindMouseEnter: function (selector, func) {
    $(selector).bind("mouseenter", func);
  },
  bindMouseLeave: function (selector, func) {
    $(selector).bind("mouseleave", func);
  },
  liveClick: function (selector, func) {
    $(selector).live("click", func);
  },
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
  init: function () {
    for (idx in this.onload_functions) {
      func = this.onload_functions[idx];
      func();
    }
  }
});

OpenLP.Namespace.create("OpenLP.Remote", {
    sendEvent: function (eventName, eventData)
    {
        var url = "/";
        if (eventName.substr(-8) == "_request")
        {
            url += "request";
        }
        else
        {
            url += "send";
        }
        url += "/" + eventName;
        var args = {};
        if (eventData != null && eventData != "")
        {
            args.q = escape(eventData);
        }
        $.ajax({
            url: url,
            dataType: "json",
            data: args,
            success: function (data)
            {
                OpenLP.Remote.handleEvent(eventName, data);
            },
            error: function (xhr, textStatus, errorThrown)
            {
                if (eventName == "remotes_poll_request")
                {
                    OpenLP.Remote.handleEvent("remotes_poll_request");
                }
            }
        });
    },
    handleEvent: function (eventName, eventData)
    {
        switch (eventName)
        {
            case "servicemanager_list_request":
                var table = $("<table>");
                $.each(eventData, function (row, item) {
                    var trow = $("<tr>")
                        .attr("value", parseInt(row))
                        .click(OpenLP.Remote.sendSetItem);
                    if (item["selected"])
                    {
                        trow.addClass("selected");
                    }
                    trow.append($("<td>").text(parseInt(row) + 1));
                    trow.append($("<td>").text(item["title"]));
                    trow.append($("<td>").text(item["plugin"]));
                    trow.append($("<td>").text("Notes: " + item["notes"]));
                    table.append(trow);
                });
                $("#service").html(table);
                break;
            case "slidecontroller_live_text_request":
                var table = $("<table>");
                $.each(eventData, function (row, item) {
                    var trow = $("<tr>")
                        .attr("value", parseInt(row))
                        .click(OpenLP.Remote.sendLiveSet);
                    if (item["selected"])
                    {
                        trow.addClass("selected");
                    }
                    trow.append($("<td>").text(item["tag"]));
                    trow.append($("<td>").html(item["text"] ? item["text"].replace(/\\n/g, "<br />") : ""));
                    table.append(trow);
                });
                $("#current-item").html(table);
                break;
            case "remotes_poll_request":
                OpenLP.Remote.sendEvent("remotes_poll_request");
                OpenLP.Remote.sendEvent("servicemanager_list_request");
                OpenLP.Remote.sendEvent("slidecontroller_live_text_request");
                break;
        }
    },
    sendLiveSet: function (e)
    {
        var tr = OpenLP.Events.getElement(e).parent();
        if (tr[0].tagName != "TR")
        {
            tr = tr.parent();
        }
        OpenLP.Remote.sendEvent("slidecontroller_live_set", tr.attr("value"));
        return false;
    },
    sendSetItem: function (e)
    {
        var id = OpenLP.Events.getElement(e).parent().attr("value");
        OpenLP.Remote.sendEvent("servicemanager_set_item", id);
        return false;
    },
    sendAlert: function (e)
    {
        var alert_text = $("#alert-text").val();
        OpenLP.Remote.sendEvent("alerts_text", alert_text);
        return false;
    },
    buttonClick: function (e)
    {
        var id = OpenLP.Events.getElement(e).attr("id");
        OpenLP.Remote.sendEvent(id);
        return false;
    }
});

OpenLP.Events.bindLoad(function () {
    OpenLP.Events.bindClick("input[type=button][id!=alert-send]", OpenLP.Remote.buttonClick);
    OpenLP.Events.bindClick("#alert-send", OpenLP.Remote.sendAlert);
    OpenLP.Remote.sendEvent("servicemanager_list_request");
    OpenLP.Remote.sendEvent("slidecontroller_live_text_request");
    OpenLP.Remote.sendEvent("remotes_poll_request");
});
