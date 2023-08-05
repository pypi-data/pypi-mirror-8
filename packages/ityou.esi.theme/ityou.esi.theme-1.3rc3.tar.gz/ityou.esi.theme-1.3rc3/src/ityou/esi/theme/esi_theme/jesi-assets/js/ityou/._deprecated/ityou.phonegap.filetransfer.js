(function($, window, document, _, undefined) {
	'use strict';
	
	window.ityouPhonegapFileTransfer = {
		name: 'ityou.phonegap.filetransfer',
		version: '0.1.2',
		settings: {
			parent: '',
			download_dom: '',
			status_dom: ''
		},
		cache: {},
		_progress_download: function() {
			var self = this;
			
			self.cache.fileTransfer.onprogress = function(progressEvent) {
				if(progressEvent.lengthComputable) {
					var loaded = device.platform == 'Android' ? progressEvent.loaded / 2 : progressEvent.loaded;
					
					var perc = Math.floor(loaded / progressEvent.total * 100);
					
					
					self.settings.parent.find(self.settings.status_dom)
						.show()
							.find('.progress-bar')
							.attr('style', 'width:'+perc+'%;');
					self.settings.parent.find(self.settings.status_dom).find('span.sr-only').text(perc + '%');
				} else {
					if(self.settings.parent.find(self.settings.status_dom).text().length == 0) {
						self.settings.parent.find(self.settings.status_dom).text('Loading');
						self.settings.parent.find(self.settings.status_dom).find('span.sr-only').text('Loading');
					} else {
						self.settings.parent.find(self.settings.status_dom).find('span.sr-only')
							.text(self.settings.parent.find(self.settings.status_dom).find('span.sr-only').text() + '.');
					}
				}
			}
			
			self.cache.fileTransfer.download(self.cache.uri, self.cache.downloadPath, function(entry) {
				self.settings.parent.find(self.settings.status_dom).find('.progress').hide();
				self.settings.parent.find(self.settings.status_dom).find('.download-finished').fadeIn(100);
				
				self.cache.uploadedFile = entry.fullPath;
				_.__debug('download complete:', entry.fullPath);
			}, function(error) {
				_.__debug('download error source:', error.source);
				_.__debug('download error target:', error.target);
				_.__debug('upload error code:', error.code);
			});
		},
		_start_download: function() {
			var self = this;
			
			self.cache.fileTransfer = new FileTransfer();
			self.cache.uri = encodeURI(self.cache.path);
			
			self.cache.fileSystem.root.getDirectory('Download', {create: false, exclusive: false}, function(parent) {
				self.cache.downloadPath = self.cache.fileSystem.root.fullPath + '/' + parent.name + '/' + self.cache.path.split('/')[self.cache.path.split('/').length-1];
				self._progress_download();
			}, function(error) {
				self.cache.downloadPath = self.cache.fileSystem.root.fullPath + '/' + self.cache.path.split('/')[self.cache.path.split('/').length-1];
				self._progress_download();
			});
		},
		init: function() {
			var self = this;
			
			window.requestFileSystem(LocalFileSystem.PERSISTENT, 0, function(filesystem) {
				self.cache.fileSystem = filesystem;
				self._start_download();
			}, function(error) {
				_.__debug('Failed @ getting LocalFileSystem');
			});
		}
	};
	
	$.fn.ityouPhonegapFileTransfer = function(opts) {
		var _self = ityouPhonegapFileTransfer;
		
		if(opts instanceof Object) {
			if(opts.settings instanceof Object) {
				$.extend(_self.settings, opts.settings);
			}
			
			if(opts.cache instanceof Object) {
				$.extend(_self.cache, opts.cache);
			}
		}
		
		_self.init();
	}
}(jQuery, this, this.document, this.ityou));
