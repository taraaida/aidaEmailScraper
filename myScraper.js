//Import the system, webpage, and fs modules so that we can get arguments from console
//write to a text file and scrape a websites HTML
var system = require('system')
var webPage = require('webpage');
var fs = require('fs');



//Get the hyperlink to scrape
var link = system.args[1]

//create and open the page
var page = webPage.create(); 
page.open(link, function(status){
  
  // return the innerHTML
  var bodyHTML = page.evaluate(function() {
    return document.body.innerHTML; 

  });

  //write HTML to text file
  fs.write("tempPage.txt", bodyHTML);
  phantom.exit();

}); 

