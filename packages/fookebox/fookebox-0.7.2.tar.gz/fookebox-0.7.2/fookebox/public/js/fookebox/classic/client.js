/*
 * fookebox, https://github.com/cockroach/fookebox
 *
 * Copyright (C) 2007-2014 Stefan Ott. All rights reserved.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

"use strict";

function Message(text)
{
	this.text = text;
}

Message.prototype.show = function()
{
	if ($('#messageText').data('timeout'))
	{
		clearTimeout($('#messageText').data('timeout'));
	}

	$('#messageText').text(this.text);
	$('#messageText').data('timeout', setTimeout(this.hide, 3000));
	$('#message').show();
}

Message.prototype.hide = function()
{
	$('#message').fadeOut('slow');
}

function AjaxView()
{
}

AjaxView.prototype.get = function(url, cb)
{
	$.ajax({
		url: url,
		type: 'GET',
		success: $.proxy(cb, this),
		error: $.proxy(this.ajaxError, this)
	});
}

AjaxView.prototype.post = function(url, data, cb, fcb)
{
	if (!cb)
		cb = this.ignore;

	if (!fcb)
		fcb = this.ajaxError;

	$.ajax({
		url: url,
		type: 'POST',
		data: JSON.stringify(data),
		contentType: 'application/json; charset=utf-8',
		success: $.proxy(cb, this),
		error: $.proxy(fcb, this)
	});
}

AjaxView.prototype.ajaxError = function(data)
{
	new Message(data.statusText).show();
	$('#progress').hide();
}

AjaxView.prototype.ignore = function(data)
{
}

function QueueView(songRemoval)
{
	this.songRemoval = songRemoval;
	this.queueLength = -1;
	this.queueView = $('#playlist');
	this.template = '<span class="artist"></span> - <span class="title"></span>';
}

QueueView.prototype = new AjaxView();

QueueView.prototype.sync = function()
{
	this.get('queue', this.update);
	$('#progress').hide();
}

QueueView.prototype.update = function(data)
{
	var queue = data.queue;
	this.queueLength = queue.length;

	var playlist = this.queueView.find('li');

	playlist.each(function(i, li)
	{
		var item = queue[i];

		if (item) {
			this.updateSlot($(li), i, item);
		} else {
			$(li).html('<span class="freeSlot">-- ' +
						_('empty') + ' --</span>');
		}
	}.bind(this));
}

QueueView.prototype.updateSlot = function(element, position, track)
{
	if (!track.artist || (track.artist == ''))
		track.artist = _('Unknown artist');
	if (!track.title || (track.title == ''))
		track.title = _('Unnamed track');

	element.html(this.template);
	element.find('.artist').text(track.artist);
	element.find('.title').text(track.title);

	if (this.songRemoval)
	{
		var link = $('<a href="#"></a>');
		link.click($.proxy(function()
		{
			this.unqueue(position + 1);
			return false;
		}, this));

		var img = $('<img src="img/classic/delete.png" alt="x" />');
		img.attr('title', _('Remove from the queue'));
		link.append(img);
		element.append(link);
	}
}

QueueView.prototype.setLength = function(length)
{
	if (length != this.queueLength)
		this.sync();
}

QueueView.prototype.unqueue = function(id)
{
	$('#progress').show();
	this.post('remove', {'id': id}, this.sync);
}

function TrackView()
{
	this.artist = "";
	this.track = "";
	this.timeTotal = "00:00";
	this.playing = false;

	this.time = new Date(0, 0, 0);
}

TrackView.prototype.attach = function(jukebox)
{
	this.artistView = $('#artist');
	this.trackView = $('#track');
	this.timeView = $('#timeTotal');
	this.timePassedView = $('#timePassed');

	function addControl(key)
	{
		$('#control-' + key).click(function()
		{
			jukebox.control(key);
			return false;
		});
	}

	if ($('#control')) {
		addControl('prev');
		addControl('pause');
		addControl('play');
		addControl('next');
		addControl('voldown');
		addControl('volup');
		addControl('rebuild');
	}
}

TrackView.prototype.updateTime = function()
{
	var seconds = this.time.getSeconds();
	var minutes = this.time.getMinutes();

	if (seconds < 10)
		seconds = "0" + seconds;
	if (minutes < 10)
		minutes = "0" + minutes;

	this.timePassedView.text(minutes + ":" + seconds);
}

TrackView.prototype.tick = function()
{
	if (this.playing)
		this.time.setSeconds(this.time.getSeconds() + 1);
	this.updateTime();
}

TrackView.prototype.adjustTime = function(time)
{
	// sync our client-side track time with the one from the
	// server. update the seconds only if we differ by more than
	// one second (force-update the display in that case).
	//
	// this should fix the 'jumpy' track time display
	var parts = time.split(':');
	if (parts.length == 2)
	{
		var minutes = parts[0];
		var seconds = parts[1];

		var diff = seconds - this.time.getSeconds();

		this.time.setMinutes(minutes);

		if (diff > 1 || diff < -1)
		{
			this.time.setSeconds(seconds);
			this.updateTime();
		}
	}
}

TrackView.prototype.update = function(artist, track, timeTotal, playing)
{
	this.artist = artist;
	this.track = track;
	this.timeTotal = timeTotal;
	this.playing = playing;

	if (!this.playing)
		$('#timePassed').addClass('paused');
	else
		$('#timePassed').removeClass('paused');

	if (this.artist != this.artistView.text())
		this.artistView.text(this.artist);
	if (this.track != this.trackView.text())
		this.trackView.text(this.track);
	if (this.timeTotal != this.timeView.text())
		this.timeView.text(this.timeTotal);
}

function CoverView()
{
	this.img = $('#nowPlayingCover');
}

CoverView.prototype.setCover = function(hasCover, coverURI)
{
	if (hasCover) {
		this.img.attr('src', 'cover/' + coverURI);
		this.img.show();
	} else {
		this.img.hide();
	}
}

function MusicView(jukebox)
{
	this.jukebox = jukebox;
}

MusicView.prototype = new AjaxView();

MusicView.prototype.attach = function()
{
	$('.artistLink').each(function(link)
	{
		link.onclick = function() {
			var target = event.target;
			var artist = target.id.substring(7, target.id.length);
			this.showArtist(artist);
			return false;
		}.bind(this);
	}.bind(this));

	$('.genreLink').each(function(link)
	{
		link.onclick = function() {
			var target = event.target;
			var genre = target.id.substring(6, target.id.length);
			this.showGenre(genre);
			return false;
		}.bind(this);
	}.bind(this));

	var searchForm = $('#searchForm');

	if (searchForm)
	{
		searchForm.submit($.proxy(function(event)
		{
			var form = event.target;
			this.search(form);
			return false;
		}, this));
	}
}

MusicView.prototype.showArtist = function(artist)
{
	$('#progress').show();

	// TODO: the page control should actually do this
	window.location = "#artist=" + artist;
	this.jukebox.page.url = window.location.href;

	this.get('artist/' + artist, this.showSearchResult);
}

MusicView.prototype.showGenre = function(genre)
{
	$('#progress').show();

	// TODO: the page control should actually do this
	window.location = "#genre=" + genre;
	this.jukebox.page.url = window.location.href;

	this.get('genre/' + genre, this.showSearchResult);
}

MusicView.prototype.search = function(form)
{
	$('#progress').show();

	var data = {
		'where': $('#searchType').val(),
		'what':  $('#searchTerm').val(),
		'forceSearch': true
	};

	this.post('search', data, this.showSearchResult);
}

MusicView.prototype.showSearchResult = function(transport)
{
	var result = new SearchResult(this.jukebox, transport);
	result.show();

	$('#progress').hide();
}

function AlbumCover(album, target)
{
	this.album = album;
	this.target = target;
}

AlbumCover.prototype = new AjaxView();

AlbumCover.prototype.load = function()
{
	var data = {
		'artist': this.album.artist,
		'album': this.album.name
	};

	this.post('findcover', data, this.loaded, this.hide);
}

AlbumCover.prototype.loaded = function(response)
{
	this.target.attr('src', 'cover/' + response.uri);
	this.target.show();
}

AlbumCover.prototype.hide = function(transport)
{
	this.target.hide();
}

function SearchResult(jukebox, data)
{
	this.jukebox = jukebox;

	this.tracks = data.tracks;
	this.what = data.meta.what;

	if (!this.what || (this.what == ''))
		this.what = _('(none)');

	this.albums = {}

	this.albumTemplate = '<span class="artist"></span> - <span class="name"></span>';
	this.albumDiscTemplate = '<span class="artist"><span> - <span class="name"></span> (Disc#<span class="disc"></span>';

	this.parseAlbums();
}

SearchResult.prototype.parseAlbums = function()
{
	function mkstring(input)
	{
		if (typeof input == "object")
		{
			if (input.length > 0)
				return input[0];
			return "";
		}
		else
			return input;
	}

	for (var key in this.tracks)
	{
		var track = this.tracks[key];
		// Yes, this sucks: python-mpd enjoys returning arrays
		// when multiple tags are present. We need to unpack
		// them here.

		track.album = mkstring(track.album);
		track.artist = mkstring(track.artist);
		track.title = mkstring(track.title);
		track.track = mkstring(track.track);

		var key = track.album + "-" + track.disc;
		var album = this.albums[key];

		if (album == null)
		{
			album = new Album(track.artist, track.album,
				track.disc);
			this.albums[key] = album;
		}

		album.add(track);
	}
}

SearchResult.prototype.showTrack = function(track)
{
	var node = $('<li class="track"></li>');
	var link = $('<a href="#"></a>');

	var template = '<span class="track"></span> - <span class="artist"></span> - <span class="title"></span>';
	link.html(template);

	link.find('.track').text(track.track);
	link.find('.artist').text(track.artist);
	link.find('.title').text(track.title);

	link.click($.proxy(function(event)
	{
		this.jukebox.queue(track);
		return false;
	}, this));

	node.append(link);
	return node;
}

SearchResult.prototype.showAlbum = function(album)
{
	var node = $('<li class="searchResultItem"></li>');
	var header = $('<h3 class="album"></h3>');
	var tracks = $('<ul class="trackList"></ul>');
	var coverArt = $('<img class="coverArt" width="200" />');

	if (this.jukebox.config.enable_queue_album)
	{
		var link = $('<a href="#"></a>');

		link.click($.proxy(function(event)
		{
			this.jukebox.queueAlbum(album);
			return false;
		}, this));

		var template = album.disc ? this.albumDiscTemplate :
						this.albumTemplate;
		link.html(template);

		link.find('.artist').text(album.artist);
		link.find('.name').text(album.name);
		link.find('.disc').text(album.disc);

		header.append(link);
	}
	else
	{
		header.html(this.albumTemplate);
		header.find('.artist').text(album.artist);
		header.find('.name').text(album.name);
	}

	album.getTracks().forEach(function(track)
	{
		tracks.append(this.showTrack(track));
	}, this);

	if (this.jukebox.config.show_cover_art)
		new AlbumCover(album, coverArt).load();

	node.append(coverArt);
	node.append(header);
	node.append(tracks);
	return node;
}

SearchResult.prototype.show = function()
{
	// TODO: this, right
	$('#searchResult').empty();

	var header = $('<h2></h2>');
	header.text(this.what);
	var ul = $('<ul id="searchResultList"></ul>');

	var albums = new Array();
	for (var key in this.albums)
	{
		albums.push(this.albums[key]);
	}

	var sorted = albums.sort(function(a, b)
	{
		var strA = a.artist + ' - ' + a.name;
		var strB = b.artist + ' - ' + b.name;

		return strA > strB;
	});

	sorted.forEach(function(album)
	{
		ul.append(this.showAlbum(album));
	}, this);

	$('#searchResult').append(header);
	$('#searchResult').append(ul);
}

function Album(artist, name, disc)
{
	this.artist = artist;
	this.name = name;
	this.disc = disc;
	this.tracks = {};

	if (!this.artist || (this.artist == ""))
		this.artist = _('Unknown artist');
	if (!this.name || (this.name == ""))
		this.name = _('Unnamed album');
}

Album.prototype.add = function(track)
{
	if (!track.track || (track.track == ''))
		track.track = '00';
	else if (track.track.indexOf('/') >= 0)
		track.track = track.track.replace(/\/.*/, '');
	else if (track.track.length < 2)
		track.track = '0' + track.track;

	if (!track.artist || (track.artist == ""))
		track.artist = _('Unknown artist');
	if (!track.title || (track.title == ""))
		track.title = _('Unnamed track');

	if ((track.artist != this.artist) &&
				!(track.artist.indexOf(this.artist) == 0))
	{
		if (this.artist.indexOf(track.artist) == 0)
			this.artist = track.artist;
		else
			this.artist = _('Various artists');
	}

	this.tracks[track.file] = track;
}

Album.prototype.getTracks = function()
{
	var tracks = new Array();

	for (var key in this.tracks)
	{
		tracks.push(this.tracks[key]);
	}

	tracks.sort(function(a, b)
	{
		return a.track - b.track;
	});

	return tracks;
}

function JukeboxView(config)
{
	this.config = {};
	this.loadconfig();

	this.queueView = new QueueView(this.config.enable_song_removal);
	this.trackView = new TrackView();
	this.coverView = new CoverView();
	this.musicView = new MusicView(this);
	this.page = new PageControl(this);
	this.page.watch();
}

JukeboxView.prototype = new AjaxView();

JukeboxView.prototype.loadconfig = function()
{
	var body = $('body');
	this.config.enable_queue_album = (body.data('enablequeuealbum') == 'True');
	this.config.show_cover_art = (body.data('showcoverart') == 'True');
	this.config.enable_song_removal = (body.data('enablesongremoval') == 'True');
}

JukeboxView.prototype.attach = function()
{
	this.trackView.attach(this);
	this.musicView.attach();
}

JukeboxView.prototype.readStatus = function(data)
{
	this.trackView.update(data.artist, data.track, data.timeTotal,
							data.playing);
	this.trackView.adjustTime(data.timePassed);
	this.coverView.setCover(data.has_cover, data.cover_uri);
	this.queueView.setLength(data.queueLength);
}

JukeboxView.prototype.sync = function()
{
	window.setTimeout(this.sync.bind(this), 1000);

	// update time
	this.trackView.tick();

	this.get('status', this.readStatus);
}

JukeboxView.prototype.control = function(action)
{
	this.post('control', {'action': action});
}

JukeboxView.prototype.queue = function(track)
{
	this.queueAll(new Array(track.file));
}

JukeboxView.prototype.queueAlbum = function(album)
{
	window.x = album.getTracks();
	this.queueAll(album.getTracks().map(function(item)
	{
		return item.file;
	}));
}

JukeboxView.prototype.queueAll = function(tracks)
{
	$.ajax({
		url: 'queue',
		type: 'POST',
		data: JSON.stringify({'files': tracks}),
		contentType: 'application/json; charset=utf-8',
		headers: {
			accept: "application/json; charset=utf-8",
		},
		success: $.proxy(this.queueView.sync, this.queueView),
		error: this.ajaxError
	});
}

JukeboxView.prototype.showArtist = function(artist)
{
	// TODO: remove this
	this.musicView.showArtist(artist);
}

JukeboxView.prototype.showGenre = function(genre)
{
	// TODO: remove this
	this.musicView.showGenre(genre);
}

function PageControl(jukebox)
{
	this.tab = 'artist';
	this.url = '';
	this.jukebox = jukebox;
}

PageControl.prototype.watch = function()
{
	this.url = window.location.href;
	this.apply();
	this.update();

	this.attachToTab('artist');
	this.attachToTab('genre');
	this.attachToTab('search');
}

PageControl.prototype.attachToTab = function(tab)
{
	var li = $(tab + 'Tab');

	if (!li)
		return;

	var a = li.select('a');

	if (a.length > 0) {
		a[0].onclick = function() {
			this.setTab(tab);
			return false;
		}.bind(this);
	}
}

PageControl.prototype.update = function()
{
	setTimeout(this.update.bind(this), 400);

	var url = window.location.href;

	if (url != this.url)
	{
		this.url = url;
		this.apply();
	}
}

PageControl.prototype.apply = function()
{
	var url = unescape(this.url);

	if (url.indexOf("#") > -1)
	{
		var parts = url.split('#');
		var params = parts[1].split('=');
		var key = params[0];
		var value = parts[1].substring(key.length + 1);

		if (key == 'artist') {
			this.setTab(key);
			this.jukebox.showArtist(value);
		} else if (key == 'genre') {
			this.setTab(key);
			this.jukebox.showGenre(value);
		} else if (key == 'tab') {
			this.setTab(value);
		}
	}
},

PageControl.prototype.setTab = function(name)
{
	if (name == this.tab) return;

	$('#' + name + 'List').show();
	$('#' + this.tab + 'List').hide();

	$('#' + name + 'Tab').removeClass('inactive');
	$('#' + name + 'Tab').addClass('active');

	$('#' + this.tab + 'Tab').removeClass('active');
	$('#' + this.tab + 'Tab').addClass('inactive');

	this.tab = name;

	window.location = "#tab=" + name;
	this.url = window.location.href;
}

$(document).ready(function()
{
	var jukebox = new JukeboxView();
	jukebox.attach();
	jukebox.sync();
});
