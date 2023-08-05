function ClientTimezone() {
	this.client_timezone = (new Date()).getTimezoneOffset() * 60 * -1;
	this.server_timezone = $('#ESI_DATA').data('ityou-server-time-offset');
	
	this.dateFormat = $('#ESI_DATA').data('ityou-time-format');
	
	this.selector = '.client-time';
	
	
	this.get = function(key) {
		if(this.hasOwnProperty(key)) {
			return this[key];
		}
		
		return undefined;
	};
}


ClientTimezone.prototype.dateSetter = function(timestamp) {
	if(undefined === timestamp || timestamp.length === 0) {
		return false;
	}
	
	var x = timestamp.split('T');
	var dmy = x[0].split('-');
	var hmsms = x[1].split(':');
	var sms = hmsms[2].split('.');
	
	return new Date(dmy[0], dmy[1]-1, dmy[2], hmsms[0], hmsms[1], sms[0], 0); 
};


ClientTimezone.prototype.convertTime = function(timestamp) {
	// older Android Browsers (Android 2.1) are not formatting ISO correctly
	//var d = new Date('2014-04-04T21:17:20.303876Z');
	//var d = new Date(timestamp);
	var d = this.dateSetter(timestamp);
	
	if(d === false) {
		return '-';
	}
	
	d.setHours(d.getHours() - d.getTimezoneOffset()/60 - this.server_timezone/3600);
	// TODO: Sommer- und Winterzeit => impossible
	
	var x = this.parseFormat(d);
	
	return x;
};



ClientTimezone.prototype.parseFormat = function(date) {
	var format = this.dateFormat;
	var tmp = new Date();
	
	//console.log(date);
	
	if(tmp.getDate() === date.getDate() && tmp.getDay() === date.getDay() && tmp.getFullYear() === date.getFullYear()) {
		return this.zeroize(date.getHours()) + ':' + this.zeroize(date.getMinutes());
	}
	
	return format
				.replace(/\%d/, this.zeroize(date.getDate()))
				.replace(/\%m/, this.zeroize((date.getMonth()+1)))
				.replace(/\%Y/, date.getFullYear())
				.replace(/\%H/, this.zeroize(date.getHours()))
				.replace(/\%M/, this.zeroize(date.getMinutes()));
};


ClientTimezone.prototype.zeroize = function(number) {
	number = parseInt(number);
	
	if(number < 10) {
		return '0' + number;
	}
	
	return number;
}