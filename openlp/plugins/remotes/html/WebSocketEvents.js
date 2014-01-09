/******************************************************************************
 * OpenLP - Open Source Lyrics Projection                                      *
 * --------------------------------------------------------------------------- *
 * Copyright (c) 2008-2014 Raoul Snyman                                        *
 * Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      *
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

/* Thanks to Ismael Celis for the original idea */

var wsEventEngine = function(url, polling_function, polling_interval)
{
    this.polling_handle = null;
    this.polling_interval = polling_interval;
    this.polling_function = polling_function;
    this.retry_handle = null;
    this.callbacks = {};

    this.fallback = function(){
        this.kill_polling();
        if(this.polling_function)
            this.polling_handle = window.setInterval(this.polling_function, this.polling_interval);
        this.kill_retries();
        var theEngine = this;
        this.retry_handle = window.setInterval(function(){theEngine.setup();}, 10000);
    }

    this.kill_polling = function(){
        if(this.polling_handle)
            window.clearInterval(this.polling_handle);
        this.polling_handle = null;
    }

    this.kill_retries = function(){
        if(this.retry_handle)
            window.clearInterval(this.retry_handle);
    }

    this.bind = function(event_name, callback){
        this.callbacks[event_name] = this.callbacks[event_name] || [];
        this.callbacks[event_name].push(callback);
        return this;
    }

    this.send = function(event_name, event_data){
        var payload = JSON.stringify({ event: event_name, data: event_data });
        this.websocket.send(payload);
        return this;
    }

    this.dispatch = function(event_name, message){
        var chain = this.callbacks[event_name];
        if(typeof chain == 'undefined') return; // no callbacks
        for(var i = 0; i < chain.length; i++)
            chain[i](message);
    }

    this.setup = function(){
        this.websocket = new WebSocket(url);
        this.websocket.engine = this;

        this.websocket.onmessage = function(websocket_msg){
            if(this.engine.polling_function)
                this.engine.polling_function();
            if( websocket_msg.data.length > 0 ){
                try{
                    var json = JSON.parse(websocket_msg.data);
                    this.engine.dispatch(json.event, json.data);
                }
                catch(err){
                }
            }
        }

        this.websocket.onclose = function(){
            this.engine.dispatch('close', null);
            this.engine.fallback();
        }

        this.websocket.onopen = function(){
            this.engine.dispatch('open', null);
            this.engine.kill_polling();
            this.engine.kill_retries();
        }

    }

    if('WebSocket' in window){
        this.setup();
    }
    else{
        this.fallback();
    }

}