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
  load: function (func) {
    this.onload_functions.append(func);
  },
  click: function (selector, func) {
    $(selector).bind("click", func);
  },
  change: function (selector, func) {
    $(selector).bind("change", func);
  },
  submit: function (selector, func) {
    $(selector).bind("submit", func);
  },
  blur: function (selector, func) {
    $(selector).bind("blur", func);
  },
  paste: function (selector, func) {
    $(selector).bind("paste", func);
  },
  keyup: function (selector, func) {
    $(selector).bind("keyup", func);
  },
  keydown: function (selector, func) {
    $(selector).bind("keydown", func);
  },
  keypress: function (selector, func) {
    $(selector).bind("keypress", func);
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
    sendEvent: function (event_name, event_data)
    {
        return false;
    }
});