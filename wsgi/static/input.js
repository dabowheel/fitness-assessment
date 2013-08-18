function isNumeric(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

function OneAndHalfRun(sex,weight,weightUnits,time,heartRate) {
	if (sex == "male" || sex == "female") {
		this.sex = sex;
	}
	if (isNumeric(weight)) {
		this.weight = weight;
	}
	if (weightUnits == "lbs" || weightUnits == "kg") {
		this.weightUnits = weightUnits;
	}
	if (isNumeric(time)) {
		this.time = time;
	}
	if (isNumeric(heartRate)) {
		this.heartRate = heartRate;
	}
}
OneAndHalfRun.prototype.weightUnit="lbs";
OneAndHalfRun.prototype.toString = function (){
	var str = "";
	if (typeof this.sex != 'undefined') {
		str = str + "sex: " + this.sex + "\n";
	}
	if (typeof this.weight != 'undefined') {
		str = str + "weight: " + this.weight + " " + this.weightUnits + "\n";
	}
	if (typeof this.time != 'undefined') {
		str = str + "time: " + this.time + "\n";
	}
	if (typeof this.heartRate != 'undefined') {
		str = str + "heartRate: " + this.heartRate + "\n";
	}
	return str;	
};
OneAndHalfRun.prototype.isValid = function () {
	if (typeof this.sex != 'undefined') {
		if (typeof this.weight != 'undefined') {
			if (typeof this.time != 'undefined') {
				if (typeof this.heartRate != 'undefined') {
					return true;
				}
			}
		}
	}
	return false;
};
/* 
 * V02max = 100.5 + 8.344 * GENDER (0 = female; I = male) - 0.1636 * BODY MASS (kg) - 1.438 * JOG TIME (min 1 mile) - 0.1928 * HEART RATE (bpm)
 */
OneAndHalfRun.prototype.calculate = function () {
	var gender;
	var weight;
	
	if (this.sex == "male") {
		gender = 1;
	} else {
		gender = 0;
	}
	
	if (this.weightUnits == "kg") {
		weight = this.weight;
	} else if (this.weightUnits == "lbs") {
		var kgPerLbs = 0.453592;
		weight = kgPerLbs * this.weight;
	}
	return 100.5 + 8.344 * gender - 0.1636 * weight - 1.438 * this.time - 0.1928 * this.heartRate;
};

function round(num) {
	return Math.round(num * 100) / 100;
}


function getMetric() {
	var sex = document.getElementById("sex");
	var weight = document.getElementById("weight");
	var weightUnit = document.getElementById("weightUnit");
	var time = document.getElementById("time");
	var heartRate = document.getElementById("heartRate");
	
	var weightUnitValue = weightUnit.options[weightUnit.selectedIndex].value;
	
	return new OneAndHalfRun(sex.value,weight.value,weightUnitValue,time.value,heartRate.value);
}
function onChange() {
	var metric = getMetric();
	var result = document.getElementById("result");
	
	if (metric.isValid()) {
		result.value = round(metric.calculate());
	} else {
		result.value = "";
	}
}

function saveEntry() {
	var metric = getMetric();
	
	if (!metric.isValid()) {
		return;
	}
	
	var vo2max = document.getElementById("vo2max");
	var result = document.getElementById("result");
	vo2max.value = result.value;
	var form = document.getElementById("entryForm");
	if (vo2max.value.length > 0) {
		form.submit();
	} else {
		alert("There are one or more fields that are not entered.")
	}
}
