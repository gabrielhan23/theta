newField = 1;

function addField(){
  var newInput = $("<li><table class='' id='pickupTimes-"+newField+"'><tbody><tr><th><label for='pickupTimes-"+newField+"-start'>Start Date</label></th><td><input id='pickupTimes-"+newField+"-start' name='pickupTimes-"+newField+"-start' required='' type='datetime-local' value=''></td></tr><tr><th><label for='pickupTimes-"+newField+"-end'>End Date</label></th><td><input id='pickupTimes-"+newField+"-end' name='pickupTimes-"+newField+"-end' required='' type='datetime-local' value=''></td></tr></tbody></table></li>")
  //.attr('id', 'pickupTimes-'+newField).attr('class', 'form-control form-control-lg mt-3')
  $('#pickupTimes').append(newInput);
}

