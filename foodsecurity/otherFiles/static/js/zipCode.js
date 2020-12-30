function move(){
  zip = document.getElementById("zip").value
  if (isNumeric(zip)){
    window.location.href = "https://foodsecurity.1234567890hihi.repl.co/customer/"+zip
  } else {
    document.getElementById("zip").className = "form-control form-control-lg is-invalid"
    document.getElementById("errors").innerHTML = "<span>Input is not a number</span>"
  }
  
}

function isNumeric(str) {
  if (typeof str != "string") return false
  return !isNaN(str) && !isNaN(parseFloat(str)) 
}